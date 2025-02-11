from django.shortcuts import redirect, render
from .models import Constructor, ObraPublica, Presupuesto, FechaInicio
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def inicio (request): #funcion para presentar en pantalla el codigo html del template inicio.html
    return render(request,'inicio.html')

def nuevoConstructor(request):
    return render(request, 'nuevoConstructor.html')  # Ajustado para tu estructura

def listadoConstructores(request):
    constructores = Constructor.objects.all()  # Recupera los datos de los buses
    return render(request, 'listadoConstructores.html', {'constructores': constructores})

def guardarConstructor(request):
    if request.method == 'POST':
        # Obtención de los datos del formulario
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        foto = request.FILES.get("txt_foto")
        cedula = request.POST.get('txt_cedula')
        direccion = request.POST.get('txt_direccion')
        telefono = request.POST.get('txt_telefono')
        email = request.POST.get('txt_email')

        # Verifica si ya existe un constructor con el mismo RFC
        if Constructor.objects.filter(cedula=cedula).exists():
            messages.error(request, "Ya existe un constructor con la cedula proporcionado.")
            return redirect('nuevoConstructor')  # Redirige al formulario para intentar nuevamente

        # Si no existe, crea el nuevo constructor
        nuevoConstructor = Constructor.objects.create(
            nombre=nombre, apellido=apellido, foto=foto, cedula=cedula, direccion=direccion, telefono=telefono, email=email
        )
        messages.success(request, "Constructor guardado exitosamente.")

        # Preparar correo de confirmación
        asunto = "Confirmación de registro del nuevo constructor"
        mensaje = f"""
        Hola {nombre} {apellido},

        Hemos recibido la siguiente información de tu registro:

        Cédula: {cedula}
        Dirección: {direccion}
        Teléfono: {telefono}
        Email: {email}

        Gracias por unirte a nuestro equipo de constructores.

        Atentamente,
        El equipo de gestión de constructores
        """
        
        correo = EmailMessage(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [email],  # Enviar al correo del constructor
        )

        # Adjuntar foto si está presente
        if foto:
            try:
                foto.open()  # Asegúrate de que el archivo esté abierto
                correo.attach(foto.name, foto.read(), foto.content_type)
                foto.close()  # Cierra el archivo después de leerlo
            except Exception as e:
                messages.error(request, f"Error al adjuntar el archivo: {e}")

        # Intentar enviar el correo
        try:
            correo.send()
            
        except Exception as e:
            messages.error(
                request,
                f"El constructor fue registrado, pero no se pudo enviar el correo de confirmación. Error: {e}",
            )

        # Redirigir al listado de constructores
        return redirect('listadoConstructores')

    else:
        messages.error(
            request, "Ocurrió un error al intentar guardar el constructor. Por favor, intenta nuevamente."
        )
        return redirect('nuevoConstructor')


def eliminarConstructor(request,id):
    constructorEliminar=Constructor.objects.get(id=id)
    constructorEliminar.delete()
    messages.success(request,"Constructor eliminado Exitosamente")
    return redirect('/listadoConstructores')

def editarConstructor(request, id):
    constructor = get_object_or_404(Constructor, id=id)
    return render(request, "editarConstructor.html", {'constructor': constructor})

def procesarEdicionConstructor(request, id):
    constructor = get_object_or_404(Constructor, id=id)

    # Actualizar los demás campos
    constructor.nombre = request.POST.get('txt_nombre')
    constructor.apellido = request.POST.get('txt_apellido')
    constructor.cedula = request.POST.get('txt_cedula')
    constructor.direccion = request.POST.get('txt_direccion')
    constructor.telefono = request.POST.get('txt_telefono')
    constructor.email = request.POST.get('txt_email')

    # Verificar si se ha subido una nueva foto
    if 'txt_foto' in request.FILES:
        constructor.foto = request.FILES['txt_foto']

    # Guardar los cambios
    constructor.save()
    messages.success(request, "Datos del constructor actualizados correctamente.")
    return redirect('listadoConstructores')


def nuevaObraPublica(request):
    constructores = Constructor.objects.all()  # Recupera todos los constructores
    return render(request, 'nuevaObraPublica.html', {'constructores': constructores})

def listadoObrasPublicas(request):
    obras = ObraPublica.objects.all()  # Recupera todos los registros de obras públicas
    return render(request, 'listadoObrasPublicas.html', {'obras': obras})

def guardarObraPublica(request):
    if request.method == 'POST':
        # Obtención de los datos del formulario
        nombre = request.POST.get('txt_nombre')
        ubicacion = request.POST.get('txt_ubicacion')
        descripcion = request.POST.get('txt_descripcion')
        estado = request.POST.get('txt_estado')
        constructor_id = request.POST.get('txt_constructor')

        # Verifica si ya existe una obra con el mismo nombre (puedes cambiar esta validación si lo deseas)
        if ObraPublica.objects.filter(nombre=nombre).exists():
            messages.error(request, "Ya existe una obra con ese nombre.")
            return redirect('nuevaObraPublica')  # Redirige al formulario para intentar nuevamente

        # Si no existe, crea la nueva obra pública
        constructor = get_object_or_404(Constructor, id=constructor_id)
        nuevaObra = ObraPublica.objects.create(
            nombre=nombre,
            ubicacion=ubicacion,
            descripcion=descripcion,
            estado=estado,
            constructor=constructor
        )
        messages.success(request, "Obra pública guardada exitosamente.")
        return redirect('listadoObrasPublicas')  # Redirige al listado de obras públicas
    else:
        return redirect('nuevaObraPublica')

def eliminarObraPublica(request, id):
    obraEliminar = get_object_or_404(ObraPublica, id=id)
    obraEliminar.delete()
    messages.success(request, "Obra pública eliminada exitosamente")
    return redirect('/listadoObrasPublicas')

def editarObraPublica(request, id):
    obra = get_object_or_404(ObraPublica, id=id)
    constructores = Constructor.objects.all()  # Obtener todos los constructores
    return render(request, "editarObraPublica.html", {'obra': obra, 'constructores': constructores})

def procesarEdicionObraPublica(request, id):
    obra = get_object_or_404(ObraPublica, id=id)

    # Actualizar los demás campos
    obra.nombre = request.POST.get('txt_nombre')
    obra.ubicacion = request.POST.get('txt_ubicacion')
    obra.descripcion = request.POST.get('txt_descripcion')
    obra.estado = request.POST.get('txt_estado')
    
    # Si se ha seleccionado un nuevo constructor, actualizarlo
    constructor_id = request.POST.get('txt_constructor')
    if constructor_id:
        constructor = get_object_or_404(Constructor, id=constructor_id)
        obra.constructor = constructor

    # Guardar los cambios
    obra.save()
    messages.success(request, "Datos de la obra pública actualizados correctamente.")
    return redirect('listadoObrasPublicas')


def nuevoPresupuesto(request):
    obras = ObraPublica.objects.all()  # Recupera todas las obras públicas
    return render(request, 'nuevoPresupuesto.html', {'obras': obras})

def listadoPresupuestos(request):
    presupuestos = Presupuesto.objects.all()  # Recupera todos los registros de presupuestos
    return render(request, 'listadoPresupuestos.html', {'presupuestos': presupuestos})

def guardarPresupuesto(request):
    if request.method == 'POST':
        # Obtención de los datos del formulario
        obra_id = request.POST.get('txt_obra')
        presupuesto = request.POST.get('txt_presupuesto')

        # Verifica si ya existe un presupuesto para la obra dada
        if Presupuesto.objects.filter(obra_id=obra_id).exists():
            messages.error(request, "Ya existe un presupuesto para esta obra.")
            return redirect('nuevaPresupuesto')  # Redirige al formulario para intentar nuevamente

        # Si no existe, crea el nuevo presupuesto
        obra = get_object_or_404(ObraPublica, id=obra_id)
        nuevoPresupuesto = Presupuesto.objects.create(
            obra=obra,
            presupuesto=presupuesto
        )
        messages.success(request, "Presupuesto guardado exitosamente.")
        return redirect('listadoPresupuestos')  # Redirige al listado de presupuestos
    else:
        return redirect('nuevaPresupuesto')

def eliminarPresupuesto(request, id):
    presupuestoEliminar = get_object_or_404(Presupuesto, id=id)
    presupuestoEliminar.delete()
    messages.success(request, "Presupuesto eliminado exitosamente.")
    return redirect('/listadoPresupuestos')

def editarPresupuesto(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id)
    obras = ObraPublica.objects.all()  # Obtener todas las obras públicas
    return render(request, "editarPresupuesto.html", {'presupuesto': presupuesto, 'obras': obras})

def procesarEdicionPresupuesto(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id)

    # Actualizar el presupuesto
    presupuesto.presupuesto = request.POST.get('txt_presupuesto')
    
    # Si se ha seleccionado una nueva obra, actualizarla
    obra_id = request.POST.get('txt_obra')
    if obra_id:
        obra = get_object_or_404(ObraPublica, id=obra_id)
        presupuesto.obra = obra

    # Guardar los cambios
    presupuesto.save()
    messages.success(request, "Datos del presupuesto actualizados correctamente.")
    return redirect('listadoPresupuestos')

def nuevaFechaInicio(request):
    obras = ObraPublica.objects.all()  # Recupera todas las obras públicas
    return render(request, 'nuevaFechaInicio.html', {'obras': obras})

def listadoFechasInicio(request):
    fechas_inicio = FechaInicio.objects.all()  # Recupera todos los registros de fechas de inicio
    return render(request, 'listadoFechasInicio.html', {'fechas_inicio': fechas_inicio})

def guardarFechaInicio(request):
    if request.method == 'POST':
        # Obtención de los datos del formulario
        obra_id = request.POST.get('txt_obra')
        fecha_inicio = request.POST.get('txt_fecha_inicio')

        # Verifica si ya existe una fecha de inicio para la obra dada
        if FechaInicio.objects.filter(obra_id=obra_id).exists():
            messages.error(request, "Ya existe una fecha de inicio para esta obra.")
            return redirect('nuevaFechaInicio')  # Redirige al formulario para intentar nuevamente

        # Si no existe, crea una nueva fecha de inicio
        obra = get_object_or_404(ObraPublica, id=obra_id)
        nuevaFechaInicio = FechaInicio.objects.create(
            obra=obra,
            fecha_inicio=fecha_inicio
        )
        messages.success(request, "Fecha de inicio guardada exitosamente.")
        return redirect('listadoFechasInicio')  # Redirige al listado de fechas de inicio
    else:
        return redirect('nuevaFechaInicio')

def eliminarFechaInicio(request, id):
    fechaInicioEliminar = get_object_or_404(FechaInicio, id=id)
    fechaInicioEliminar.delete()
    messages.success(request, "Fecha de inicio eliminada exitosamente.")
    return redirect('/listadoFechasInicio')

def editarFechaInicio(request, id):
    fecha_inicio = get_object_or_404(FechaInicio, id=id)
    obras = ObraPublica.objects.all()  # Obtener todas las obras públicas
    return render(request, "editarFechaInicio.html", {'fecha_inicio': fecha_inicio, 'obras': obras})

def procesarEdicionFechaInicio(request, id):
    fecha_inicio = get_object_or_404(FechaInicio, id=id)

    # Actualizar la fecha de inicio
    fecha_inicio.fecha_inicio = request.POST.get('txt_fecha_inicio')
    
    # Si se ha seleccionado una nueva obra, actualizarla
    obra_id = request.POST.get('txt_obra')
    if obra_id:
        obra = get_object_or_404(ObraPublica, id=obra_id)
        fecha_inicio.obra = obra

    # Guardar los cambios
    fecha_inicio.save()
    messages.success(request, "Fecha de inicio actualizada correctamente.")
    return redirect('listadoFechasInicio')

def listadoCompleto(request):
    # Obtener todas las obras públicas
    obras = ObraPublica.objects.all()
    
    # Crear una lista para almacenar la información combinada
    datos_combinados = []
    
    for obra in obras:
        # Obtener el constructor asociado a la obra
        constructor = obra.constructor
        
        # Obtener el presupuesto asociado a la obra (si existe)
        presupuesto = Presupuesto.objects.filter(obra=obra).first()
        
        # Obtener la fecha de inicio asociada a la obra (si existe)
        fecha_inicio = FechaInicio.objects.filter(obra=obra).first()
        
        # Crear un diccionario con la información combinada
        datos_obra = {
            'id': obra.id,  # Asegúrate de incluir el id
            'nombre_obra': obra.nombre,
            'ubicacion': obra.ubicacion,
            'estado': obra.estado,
            'constructor_nombre': f"{constructor.nombre} {constructor.apellido}" if constructor else "Sin constructor",
            'presupuesto': presupuesto.presupuesto if presupuesto else "Sin presupuesto",
            'fecha_inicio': fecha_inicio.fecha_inicio if fecha_inicio else "Sin fecha de inicio",
        }
        
        # Agregar el diccionario a la lista de datos combinados
        datos_combinados.append(datos_obra)
    
    # Pasar la lista de datos combinados al template
    return render(request, 'listadoCompleto.html', {'datos_combinados': datos_combinados})



















