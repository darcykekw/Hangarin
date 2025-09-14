from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangarinorg', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='priority',
            options={'verbose_name': 'Priority', 'verbose_name_plural': 'Priorities'},
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='priority',
            name='priority_name',
            field=models.CharField(max_length=100),
        ),
    ]
