import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic.edit import BaseDeleteView, BaseCreateView
from django.views.generic.list import BaseListView

from todo.models import Todo


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ApiTodoLV(BaseListView): # 테이블에서 데이터 가져오기
    model = Todo
    # template_name = ''
    # 요청이 get 방식으로 온다.
    # def get(self, request, *args, **kwargs):
    #     tmpList = [
    #         {'id': 1, 'name': '이창석', 'todo': '오늘 하루는 즐거운 노래로 시작해보자!!'},
    #         {'id': 2, 'name': '이순신', 'todo': '저에게 힘을 주소서!!'},
    #     ]
    #     return JsonResponse(data=tmpList, safe=False)

    def render_to_response(self, context, **response_kwargs): # 여기서 하는 일은 JsonResponse를 리턴하는 것이다.
        # get_queryset() 메서드에서 테이블로 부터 레코드를 가져와서
        todoList = list(context['object_list'].values()) # 테이블에서 가져온 레코드들을 Dict형태로 풀어준다.
        return JsonResponse(data=todoList, safe=False)


class ApiTodoDelV(BaseDeleteView): # axios.delete
    model = Todo

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object() # Todo 테이블에서 해당 레코드를 찾아서  self.object 변수에 대입
        self.object.delete() # 테이블에서 해당 레코드가 삭제된다.
        return JsonResponse(data={}, status=204) # dict 형태이기 때문에 safe=True 생략가능, status는 204로 변경


class ApiTodoCV(BaseCreateView):
    model = Todo
    fields = '__all__'
    # template name이나 sccess_url 은 JsonResponse 할 경우 필요가 없다.

    def get_form_kwargs(self): # request.body 로 받기 위해 오버라이딩 해준다.
        kwargs = super().get_form_kwargs()
        kwargs['data'] = json.loads(self.request.body) # [!] byte string을 dict 타입으로 변경해줘야 한다.
        return kwargs

    def form_valid(self, form):
        print("form_valid()", form)
        self.object = form.save() # 테이블에 새로 생성 된 레코드를 self.object 에 저장해준다.
        newTodo = model_to_dict(self.object) # self.object 타입이 모델 타입이기 때문에 dict 타입으로 변경해줘야 한다.
        print(f"newTodo: {newTodo}") # f 스트링
        return JsonResponse(data=newTodo, status=201)

    def form_invalid(self, form): # 에러내용을 http 로 전송하는
        print("form_invalid()", form)
        print("form_invalid()", self.request.POST) # print로 찍어보니 POST 에는 데이터가 들어있지 않은 걸 확인할 수 있다.
        print("form_invalid()", self.request.body.decode('utf8')) # body의 경우 byte string 타입이므로 Decode를 해준다.
        return JsonResponse(data=form.errors, status=400)