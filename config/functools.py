from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.utils import timezone
import base64

def jsonify(data):
    return json.loads(JsonResponse(data, safe=False).content)


def paginate(query_set, page_num, serializer, context, page_size=10):
    pag_obj = Paginator(query_set, page_size)
    if page_num is None:
        page = 1
    else:
        page = page_num
    main_page = pag_obj.page(page)
    data = {
        "count": pag_obj.count,
        "pages": pag_obj.num_pages,
        "result": jsonify(
            serializer(main_page.object_list, many=True, context=context).data
        ),
        "page": page,
    }
    return data


def base64_to_data(base64_data):
    format, imgstr = base64_data.split(";base64,")
    ext = format.split("/")[-1]
    suffix = timezone.now().strftime("%y%m%d_%H%M%S")
    data = ContentFile(base64.b64decode(imgstr), name="upload{}.".format(suffix) + ext)
    return data
