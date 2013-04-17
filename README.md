# PyIOC

A simple Python IOC framework. This is a stupid-simple IOC (Inversion of Control) framework.
At this time it *only* does object injection by inserting a method called **inject()**
into your objects that is used to create your dependent object variables.

As an example we have a service named **ExampleService**.

```python
class ExampleService():
	def saveInfo(self, id, newDate):
		self.exampleWebServiceFacade.save(id=id, dateModified=self.dateService.toUTC(newDate))
```

```python
import pyioc

ioc.configure(
	paths=("../model",),
	config={
		"ExampleService": {
			"dependencies": [
				"DateService",
				"ExampleWebServiceFacade"
			]
		},
		"DateService": {},
		"ExampleWebServiceFacade": {
			"dependencies": [
				"DateService"
			]
		}
	}
)

service = ioc.getBean("ExampleService")
service.saveInfo(1, datetime.now)
```

The above example shows a service object that references a web service facade object
and a date service object. These are injected into the **ExampleService** object
by PyIOC when you call **getBean()**.

## License
Copyright 2013 Adam Presley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

See the file LICENSE for more information