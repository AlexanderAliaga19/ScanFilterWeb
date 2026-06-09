# /**
#  * @author: Alexander Auden Aliaga Ocampo
#  * codigo:U202417693
#  */

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services.image_processor import (
    load_uploaded_image,
    crop_image,
    apply_filter,
    normalize_image,
    image_to_base64,
    matrix_preview,
)


def health_check(request):
    return JsonResponse({
        "message": "Backend ScanFilterWeb funcionando correctamente."
    })


@csrf_exempt
def process_image(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Este endpoint solo acepta peticiones POST."
        }, status=405)

    if not request.FILES.get("image"):
        return JsonResponse({
            "error": "No se recibió ninguna imagen."
        }, status=400)

    try:
        uploaded_image = request.FILES["image"]

        use_color = request.POST.get("use_color", "false").lower() == "true"
        crop_mode = request.POST.get("crop_mode", "crop")
        filter_name = request.POST.get("filter", "mean")

        x = int(request.POST.get("x", 0))
        y = int(request.POST.get("y", 0))

        original_image = load_uploaded_image(uploaded_image, use_color)
        selected_image = crop_image(original_image, crop_mode, x, y)

        filtered_image = apply_filter(selected_image, filter_name)
        normalized_image = normalize_image(filtered_image)

        return JsonResponse({
            "message": "Imagen procesada correctamente.",
            "filter": filter_name,
            "crop_mode": crop_mode,
            "use_color": use_color,
            "original_image": image_to_base64(original_image),
            "selected_image": image_to_base64(selected_image),
            "filtered_image": image_to_base64(normalized_image),
            "initial_matrix": matrix_preview(selected_image),
            "result_matrix": matrix_preview(normalized_image),
        })

    except ValueError as error:
        return JsonResponse({
            "error": str(error)
        }, status=400)

    except Exception as error:
        return JsonResponse({
            "error": f"Ocurrió un error inesperado: {str(error)}"
        }, status=500)