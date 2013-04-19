# Copyright 2013 Adam Presley
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import config

BEAN_PATHS = ()
IOC_CONFIG = {}

def addInjectMethod(beanName, path):
	exec "from %s import %s" % (path, beanName)
	exec "%s.inject = inject" % beanName

def configure(paths, config):
	global BEAN_PATHS
	global IOC_CONFIG

	BEAN_PATHS = paths
	IOC_CONFIG = config

	for bean in IOC_CONFIG:
		path = findBean(beanName=bean)
		if len(path) <= 0:
			raise Exception("Unable to find the bean '%s'" % bean)

def findBean(beanName):
	global BEAN_PATHS

	beanPath = ""

	for beanPath in BEAN_PATHS:
		for (path, dirs, files) in os.walk(beanPath):
			if "%s.py" % beanName in files:
				name = next((i for i in files if i == "%s.py" % beanName))
				beanPath = os.path.join(os.path.relpath(path), name)

	return beanPath

def getBean(beanName):
	global IOC_CONFIG

	if beanName not in IOC_CONFIG:
		raise Exception("The bean '%s' is not defined in IOC_CONFIG" % beanName)

	path = findBean(beanName=beanName)
	if len(path) <= 0:
		raise Exception("Unable to find the bean '%s'" % beanName)

	normalizedPath = normalizePath(path=path)

	exec "from %s import %s" % (normalizedPath, beanName)
	exec "%s.inject = inject" % beanName
	exec "bean = %s()" % (beanName,)

	if "dependencies" in IOC_CONFIG[beanName]:
		for d in IOC_CONFIG[beanName]["dependencies"]:
			bean.inject(beanName=d)

	return bean
	
def inject(self, beanName, variableName=None):
	obj = getBean(beanName=beanName)
	variableName = variableName if variableName else normalizeBeanName(beanName)
	self.__dict__[variableName] = obj

def normalizeBeanName(beanName):
	return "%s%s" % (beanName[0].lower(), beanName[1:])

def normalizePath(path):
	p,f = list(os.path.split(path))
	p = re.sub("\\.", "", p)
	f = re.sub("\\.py", "", f)

	paths = [i for i in p.split(os.sep) if len(i)]
	paths.append(f)

	result = ".".join(paths)
	return result
