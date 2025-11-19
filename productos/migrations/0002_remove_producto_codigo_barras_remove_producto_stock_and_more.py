from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sucursales", "0002_alter_sucursal_direccion_alter_sucursal_telefono"),
        ("productos", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="producto",
            name="codigo_barras",
        ),
        migrations.RemoveField(
            model_name="producto",
            name="stock",
        ),
        migrations.RemoveField(
            model_name="producto",
            name="sucursal",
        ),
        migrations.AlterField(
            model_name="producto",
            name="categoria",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="producto",
            name="nombre",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="producto",
            name="stock_minimo",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="Inventario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock", models.PositiveIntegerField(default=0)),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="productos.producto",
                    ),
                ),
                (
                    "sucursal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sucursales.sucursal",
                    ),
                ),
            ],
            options={
                "unique_together": {("producto", "sucursal")},
            },
        ),
    ]
