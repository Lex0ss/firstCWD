from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from website.forms import AddRecordForm, SignUpForm
from .models import Record


def home(request):
    records = Record.objects.all()
    
    
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticating
        user = authenticate(request, username = username,
                            password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have login')
            return redirect('home')
        else:
            messages.success(request, 'There was an error login in, try again')
            # Por lo que se ve messages es una muy buena manera de dejar mensajes dentro de plantillas HTML creadas con el motor de plantillas de Django, donde ademas
            # Estos mensajes pueden ser personalizables con CSS. Ahora, su funcionamiento es simple. solamente se escribe el tipo de mensaje que se quiere dar y este 
            # automaticamente estara disponible en la renderizacion (return render/redirect) mas cercana que tenga. Con lo cual solamente con colocarla dentro de la
            # plantilla con {{}} podra estar disponible para verse en el Frontend
            return redirect('home')
    else:
        return render(request, 'website/home.html', {'records' : records})
            
# def login_user(request):
#     return render(request, 'website/home.html')
    


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logout')
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # De esta manera el formulario obtiene los datos de el POST de la solicitud HTTP, lo que permite que este actue y use la logica interna de el formulario 
        # inmediatamente, en vez de realizar la logica aqui, como por ejemplo confirmar si un atributo de la peticion cumple cierta logica
        if form.is_valid():
            # Luego is_valid lo que hace es comprobar campo por campo si cada uno de estos cumple con las restricciones definidas en el formulario segun su logica
            # heredada o la logica que tu hayas establecido
            
            form.save()
            # save() lo que hace es tomar un tipo de variable la cual posee las caracteristicas para tomar su informacion y crear una instancia de la tabla a la cual
            # esta variable este relacionada con la informacion que esta variable puede tener  
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # cleaned_data accede al JSON que tiene los datos de el formulario y los hace accesible con claves entre corchetes
            
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, 'You have successfully registered. Welcome!!')
            return redirect('home')
    else:
        
        form = SignUpForm()
        return render(request, 'website/register.html', {'form' : form})
    
    print(request.method)
    
    return render(request, 'website/register.html', {'form' : form})
    # Entonces, la razon de este ultimo render es cuando sucedan errores. Debidos a que la logica de esta vista no gestiona las excepciones, si no que es el formulario
    # el que lo hace, entonces en caso de que exista una excepcion. Recuerda que is_valid() comprueba que no existan excepciones en el formulario, cuando una condicion
    # no se cumple dentro de un bloque, entonces el flujo de el codigo sale de este bloque, entonces, como is_valid() comprueba 1 por 1 hasta el final, cuando se da cuenta
    # que al menos hubo campo que no cumplio, entonces la condicion no se cumple, y el flujo sale de el bloque de el if de mas alto nivel, y como los errores son 
    # guardados por el formulario, entonces, esta ultima renderizacion tomara esos errores guardados y los imprimira en la plantilla segun la logica especificada alli
            
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id = pk)
        return render(request, 'website/record.html', {'customer_record' : customer_record})
    else:
        messages.error(request, 'You need to have an account')
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        deleted_record = Record.objects.get(id = pk)
        deleted_record.delete()
        messages.success(request, 'Record deleted successfuly')
        return redirect('home')
    else:
        messages.error(request, 'You must be login to delete a record')
        redirect('home')
        
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record added...')
                return redirect('home')
        return render(request, 'website/add_record.html', {'form' : form})
    else:
        messages.error(request, 'You should be logged in...')
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        #Crea el formulario que se va a cargar, donde se le cargan los campos de el registro en donde te encuentras respectivamente
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated :)')
            return redirect('home')
        return render(request, 'website/update_record.html', {'form' : form})
    else:
        messages.error(request, 'You must be logged...')
        return redirect('home')