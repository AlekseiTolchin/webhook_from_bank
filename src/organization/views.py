import json
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import Organization, Payment, BalanceLog


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    """Класс для обработки входящих webhook запросов от банка"""

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса"""
        try:
            payload = json.loads(request.body)

            validated_data = self._validate_and_parse_webhook(payload)
            if isinstance(validated_data, HttpResponse):
                return validated_data

            if self._is_duplicate_operation(validated_data['operation_id']):
                return JsonResponse({'message': 'Operation already processed'}, status=200)

            with transaction.atomic():
                self._process_payment(validated_data)

            return JsonResponse({'message': 'Operation processed successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    def _validate_and_parse_webhook(self, webhook):
        """Валидация и парсинг входящих данных"""
        try:
            operation_id = UUID(webhook['operation_id'])
            amount = Decimal(str(webhook['amount']))
            payer_inn = webhook['payer_inn']
            document_number = webhook['document_number']
            document_date = datetime.strptime(webhook['document_date'], '%Y-%m-%dT%H:%M:%SZ')
        except (KeyError, ValueError, TypeError):
            return JsonResponse({'error': 'Invalid request data'}, status=400)

        return {
            'operation_id': operation_id,
            'amount': amount,
            'payer_inn': payer_inn,
            'document_number': document_number,
            'document_date': document_date
        }

    def _is_duplicate_operation(self, operation_id):
        """Проверка на дубликаты операций"""
        return Payment.objects.filter(operation_id=operation_id).exists()

    def _process_payment(self, validated_data):
        """Обработка платежа и обновление баланса"""
        organization, created = Organization.objects.get_or_create(
            inn=validated_data['payer_inn']
        )
        if created:
            organization.balance = 0
            organization.save()

        Payment.objects.create(
            operation_id=validated_data['operation_id'],
            amount=validated_data['amount'],
            payer_inn=validated_data['payer_inn'],
            document_number=validated_data['document_number'],
            document_date=validated_data['document_date'],
            organization=organization,
        )

        self._update_balance(organization, validated_data['amount'])

    def _update_balance(self, organization, amount):
        """Обновление баланса организации и логирование изменений"""
        new_balance = organization.balance + amount
        organization.balance = new_balance
        organization.save()

        BalanceLog.objects.create(
            organization=organization,
            amount=amount,
            new_balance=new_balance
        )


class OrganizationBalanceView(View):
    """Класс для получения баланса организации по ИНН"""

    def get(self, request, inn, *args, **kwargs):
        """Обработка GET-запроса"""
        try:
            organization = Organization.objects.get(inn=inn)
            return JsonResponse({
                'inn': organization.inn,
                'balance': float(organization.balance)
            })
        except Organization.DoesNotExist:
            return JsonResponse({'message': 'Organization not found'}, status=404)
