from django.urls import path 
from . import views
urlpatterns=[
    path('', views.inicio),

    path('nuevoConstructor/', views.nuevoConstructor, name='nuevoConstructor'),  # Formulario para crear un nuevo bus
    path('listadoConstructores/', views.listadoConstructores, name='listadoConstructores'),  # Listado de buses
    path('guardarConstructor/', views.guardarConstructor, name='guardarConstructor'),
    path('eliminarConstructor/<int:id>/', views.eliminarConstructor, name='eliminarConstructor'),
    path('editarConstructor/<id>', views.editarConstructor, name="editarConstructor"),
    path('procesarEdicionConstructor/<int:id>/', views.procesarEdicionConstructor, name='procesarEdicionConstructor'),

    path('nuevaObraPublica/', views.nuevaObraPublica, name='nuevaObraPublica'),  # Formulario para crear una nueva obra pública
    path('listadoObrasPublicas/', views.listadoObrasPublicas, name='listadoObrasPublicas'),  # Listado de obras públicas
    path('guardarObraPublica/', views.guardarObraPublica, name='guardarObraPublica'),  # Guardar una nueva obra pública
    path('eliminarObraPublica/<int:id>/', views.eliminarObraPublica, name='eliminarObraPublica'),  # Eliminar obra pública
    path('editarObraPublica/<id>/', views.editarObraPublica, name="editarObraPublica"),  # Formulario para editar una obra pública
    path('procesarEdicionObraPublica/<int:id>/', views.procesarEdicionObraPublica, name='procesarEdicionObraPublica'),  # Procesar edición de obra pública

    path('nuevoPresupuesto/', views.nuevoPresupuesto, name='nuevoPresupuesto'),  # Formulario para crear un nuevo presupuesto
    path('listadoPresupuestos/', views.listadoPresupuestos, name='listadoPresupuestos'),  # Listado de presupuestos
    path('guardarPresupuesto/', views.guardarPresupuesto, name='guardarPresupuesto'),
    path('eliminarPresupuesto/<int:id>/', views.eliminarPresupuesto, name='eliminarPresupuesto'),
    path('editarPresupuesto/<id>/', views.editarPresupuesto, name='editarPresupuesto'),
    path('procesarEdicionPresupuesto/<int:id>/', views.procesarEdicionPresupuesto, name='procesarEdicionPresupuesto'),

    path('nuevaFechaInicio/', views.nuevaFechaInicio, name='nuevaFechaInicio'),
    path('listadoFechasInicio/', views.listadoFechasInicio, name='listadoFechasInicio'),
    path('guardarFechaInicio/', views.guardarFechaInicio, name='guardarFechaInicio'),
    path('editarFechaInicio/<id>/', views.editarFechaInicio, name='editarFechaInicio'),
    path('procesarEdicionFechaInicio/<int:id>/', views.procesarEdicionFechaInicio, name='procesarEdicionFechaInicio'),
    path('eliminarFechaInicio/<int:id>/', views.eliminarFechaInicio, name='eliminarFechaInicio'),

    path('listado-completo/', views.listadoCompleto, name='listadoCompleto'),
]

