# Generated by Django 4.2.17 on 2025-05-28 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.CharField(max_length=12, unique=True, verbose_name='ИНН')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Баланс')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_id', models.UUIDField(unique=True, verbose_name='id операции')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Сумма')),
                ('payer_inn', models.CharField(max_length=12, verbose_name='ИНН плательщика')),
                ('document_number', models.CharField(max_length=20, verbose_name='Номер документа')),
                ('document_date', models.DateTimeField(verbose_name='Дата документа')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='organization.organization', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Платёж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.CreateModel(
            name='BalanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Поступившая сумма')),
                ('new_balance', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Обновленный баланс')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
