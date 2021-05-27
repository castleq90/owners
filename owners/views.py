import json
from django.views import View
from django.http  import JsonResponse
from .models      import Dogs, Owners

class OwnerView(View):

    def get(self,request):
        owners = Owners.objects.all()
        
        result = []
        for owner in owners:
            dogs      = owner.dogs_set.all() # 역참조 모델 클래스명_set
            dogs_list = []

            for dog in dogs:
                dog_info = {
                    'name': dog.name,
                    'age' : dog.age
                }
                dogs_list.append(dog_info)

            # my_list = [1,2,3,4,5]
            # b = [num for num in my_list]
            # 출력문 -> b =[1,2,3,4,5]

            # dogs_list = [{
            #     'name': dog.name,
            #     'age' : dog.age
            # }for dog in dogs]


            owner_info ={
                'email': owner.email,
                'name' : owner.name,
                'age'  : owner.age,
                'dogs' : dogs_list
            }
            result.append(owner_info)

        return JsonResponse({'result': result}, status=200)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            Owners.objects.create(name=data['name'], age=data['age'], email=data['email'])

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'IVALID_KEY'}, status=400)

class DogView(View):

    def get(self,request):
        dogs = Dogs.objects.all()
        
        result = []
        for dog in dogs:
            dog_info ={
                'owner': dog.owners.name,
                'name' : dog.name,
                'age'  : dog.age
            }
            result.append(dog_info)

        return JsonResponse({'result': result}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            
            owner = Owners.objects.get(email=data['owner'])
            Dogs.objects.create(name=data['name'], age=data['age'], owners=owner)
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'IVALID_KEY'}, status=400)
        except Owners.DoesNotExist:
            return JsonResponse({'message': 'USER DOES NOT EXIST'}, status=400)