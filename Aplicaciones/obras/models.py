from django.db import models

class Constructor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    foto=models.FileField(upload_to='constructores',null=True,blank=True)
    cedula = models.CharField(max_length=10, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class ObraPublica(models.Model):
    ESTADO_OPCIONES = (
        ('planeacion', 'Planeación'),
        ('en_proceso', 'En Proceso'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    )
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=ESTADO_OPCIONES, default='planeacion')
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE, null=True, related_name="obras")

    def __str__(self):
        return f"{self.nombre} ({self.estado})"


class Presupuesto(models.Model):
    id = models.AutoField(primary_key=True)
    obra = models.ForeignKey(ObraPublica, on_delete=models.CASCADE, related_name="presupuestos")
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Aprobado")

    def __str__(self):
        return f"Presupuesto de {self.obra.nombre} - {self.presupuesto}"


class FechaInicio(models.Model):
    id = models.AutoField(primary_key=True)
    obra = models.ForeignKey(ObraPublica, on_delete=models.CASCADE, related_name="fechas_inicio")
    fecha_inicio = models.DateField()

    def __str__(self):
        return f"Fecha de inicio de {self.obra.nombre} - {self.fecha_inicio}"
