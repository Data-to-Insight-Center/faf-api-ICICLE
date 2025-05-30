# Working on the Project
## Implementing New Endpoints
###urls.py
The process of implementing new endpoints is mainly done in the Rest_API application. A resource path needs to be created in the urls.py file and needs to follow the following guidlines:
```python
path('endpoint/', name_of_class_in_views.as_view()),
```
This endpoint creation isn't complete until the class in views.py is created, as the class will be searched for the moment that the endpoint is called.
###views.py
In views.py, all of the classes are implemented with the parent calss APIView which was prebuild from rest_framework.views. This is used because:

* It allows for @extend_schema which allows the developer to design the swagger page by giving each endpoint examples, descriptions and information on what to expect to give/recieve

* APIView allows for each of the methods to be called post, get, etc. and will automatically call them when the action is needed which saves a lot on coding and readability

The @extend_schema is built from the drf_spectacular library which is needed to produce a swagger hub ui that is above version 3. The general setup is as follows:

```python
@extend_schema(
    description="",
    examples=[],
    requests=,
    responses={},
)
```
Description is mainly just for writing a description about the endpoint. Examples are just the examples you want to show, but I implemented them with OpenApiExample() which just simplified the process as it standardized the process as follows:
```pythonOpenApiExample(
    'Name of Example',
    value = Example,
    media_type="How the data is given", #I used 'text/csv'
)
```
Requests took in the serializers which will be explained after views, but that is how the information is taken in/returned from/to the user.The responses were just the expected results that I just put into a dictionary as 200 with an example of the data.
                                                                                           From here the methods are built using the common http protocols. The method name 'post' is the most commonly used because getting the data from the user requires the user to post data which is taken in by the serializers. This method I mainly use to check the serializer and then call a class that takes care of the functionaliy of creating a query, then I call Query_tool() class that has a method called quer() that actually sends the query to the MySQL server before turning the results into a pandas dataframe.

The default next step I've been doing is converting data to a csv file before shipping it with response:

```python
csv_data = data.to_csv(index=False)
response = HttpResponse(csv_data, content_type="text/csv")
response['Content-Disposition'] = f'attachment; filename=name_of_file.csv'
```

###serializers.py
As noted above in views, serializers are needed to recive (and potentially send non_downloadable data). To recieve the data in views.py, someSerializer(data=request.data) needs to be given a variable which then looks at the request data. Then the method .is_valid() is checked to make sure that the serializer was filled out which can be seen in the following example from views.py:
```python
def post(self, request):
    serializer = s.TableSerializer(data=request.data)
    if serializer.is_valid():
```
Where s is just the name I gave the imported file serializers.py.

In serializers.py, the parent class serializers from rest_framework was used just to simply the process. All that is needed to make a serializer is the child class name and whatever data you want to give the endpoint. The following is an example from the point_to_point/ endpoint:
```python
class PointToPointSerializer(serializers.Serializer):
    commodity   = serializers.CharField(max_length=40)
    origin      = serializers.CharField(max_length=40)
    destination = serializers.CharField(max_length=40)
    timeframe   = serializers.ListField(max_length=2, child=serializers.IntegerField())
```
This serializer is looking for three strings and a list of up to size 2 that contains integers only. Whenever point_to_point/ is called, the program is checking to see if this information is filled out.
