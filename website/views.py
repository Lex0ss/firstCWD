from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from website.forms import SignUpForm

def home(request):
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
        return render(request, 'website/home.html')
            
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
    
    return render(request, 'website/register.html', {'form' : form})
    
        
            