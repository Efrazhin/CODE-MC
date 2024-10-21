
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('cuit', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='CUIT')),
                ('nombre', models.CharField(max_length=100, verbose_name='Razón social')),
                ('telefono', models.CharField(max_length=50, verbose_name='Teléfono de contacto')),
                ('email', models.EmailField(max_length=254, verbose_name='Email de contacto')),
                ('descripcion', models.TextField(verbose_name='Descripción de actividades')),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id_pais', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Pais')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id_provincia', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Provincia')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id_stock', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Stock')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('dni', models.CharField(max_length=120, unique=True, verbose_name='DNI')),
                ('telefono', models.CharField(max_length=120, verbose_name='Teléfono')),
                ('rol', models.CharField(default='empleado', max_length=10, verbose_name='Rol')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='miapp_CODEMC.empresa')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jefe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado', to='miapp_CODEMC.businessmanager')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='empleado', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Compra')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empleado', verbose_name='Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('dni_cliente', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido')),
                ('calle', models.CharField(blank=True, max_length=100, null=True, verbose_name='Calle')),
                ('nro_calle', models.IntegerField(blank=True, null=True, verbose_name='Número de Calle')),
                ('telefono', models.CharField(max_length=50, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Categoría')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id_almacen', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID Almacén')),
                ('telefono', models.CharField(max_length=50, verbose_name='Teléfono')),
                ('ciudad', models.CharField(max_length=100, verbose_name='Ciudad')),
                ('calle', models.CharField(max_length=100, verbose_name='Calle')),
                ('nro_calle', models.IntegerField(verbose_name='Número de Calle')),
                ('tamaño', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tamaño')),
                ('unidad_medida', models.CharField(max_length=50, verbose_name='Unidad de Medida')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empresa')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.provincia', verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id_presupuesto', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Presupuesto')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.cliente', verbose_name='Clientes')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empleado', verbose_name='Empleados')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Producto')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('tamaño', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tamaño')),
                ('unidad_medida', models.CharField(blank=True, max_length=50, null=True, verbose_name='Unidad de Medida')),
                ('fecha_vencimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento')),
                ('almacen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.almacen')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.categoria', verbose_name='Categorías')),
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.stock', verbose_name='Stock')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePresupuesto',
            fields=[
                ('id_detalle_presupuesto', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Detalle Presupuesto')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Descuento')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Importe')),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.presupuesto', verbose_name='Presupuesto')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.producto', verbose_name='Producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id_detalle_compra', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Detalle Compra')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Importe')),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.compra', verbose_name='Compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.producto', verbose_name='Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('dni_proveedor', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='DNI')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellido')),
                ('cuit', models.CharField(blank=True, max_length=25, null=True, verbose_name='Razón social')),
                ('telefono', models.CharField(max_length=50, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('calle', models.CharField(max_length=100, verbose_name='Calle')),
                ('ciudad', models.CharField(max_length=100, verbose_name='Ciudad')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('web', models.URLField(blank=True, null=True, verbose_name='Web')),
                ('comentarios', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('nro_calle', models.IntegerField(verbose_name='Número de Calle')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empresa')),
                ('pais', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='miapp_CODEMC.pais', verbose_name='País')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.provincia', verbose_name='Provincia')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.proveedor', verbose_name='Proveedor'),
        ),
        migrations.CreateModel(
            name='Remito',
            fields=[
                ('id_remito', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Remito')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('almacen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='miapp_CODEMC.almacen', verbose_name='Almacén')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.cliente', verbose_name='Cliente')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empleado', verbose_name='Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemito',
            fields=[
                ('id_detalle_remito', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Detalle Remito')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Descuento')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Importe')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.producto', verbose_name='Almacén')),
                ('remito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.remito', verbose_name='Remito')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id_subcategoria', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Subcategoría')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.categoria', verbose_name='Categoría')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.subcategoria', verbose_name='Subcategorías'),
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id_sucursal', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID Sucursal')),
                ('telefono', models.CharField(max_length=50, verbose_name='Teléfono')),
                ('ciudad', models.CharField(max_length=100, verbose_name='Ciudad')),
                ('calle', models.CharField(max_length=100, verbose_name='Calle')),
                ('nro_calle', models.IntegerField(verbose_name='Número de Calle')),
                ('almacen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.almacen', verbose_name='Almacén')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.empresa')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.provincia', verbose_name='Provincia')),
            ],
        ),
        migrations.AddField(
            model_name='remito',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='miapp_CODEMC.sucursal', verbose_name='Sucursal'),
        ),
        migrations.AddField(
            model_name='producto',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.sucursal'),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp_CODEMC.sucursal', verbose_name='Sucursales'),
        ),
    ]
