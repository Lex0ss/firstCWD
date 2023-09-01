from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            
def login_user(request):
    pass        


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logout')
    return redirect('home')