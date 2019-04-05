import json
import requests

class GrafanaAdmin(object):
	"""
	Documentation
	"""
	def __init__(self, url):
		self.url = url
		self.verify = True

	def GrafanaAuth(self, AuthType='Normal', **kwargs):
		if 'Normal' in AuthType:
			for key in ('Username', 'Password'):
				if key in kwargs:
					setattr(self, key, kwargs[key])
				else:
					return('Using "Normal" as "AuthType", is mandatory to set "Username" and "Password". {0} is not configured.'.format(key))
			s = requests.Session()
			s.auth = (self.Username, self.Password)
			s.verify = self.verify
			setattr(self, 'Session', s)

		elif 'APIKey' in AuthType:
			if 'Key' in kwargs:
				setattr(self, 'Key', kwargs['Key'])
			else:
				return('Using "APIKey" as "AuthType", is mandatory to set "Key". {0} is not configured.'.format(key))
			s = requests.Session()
			s.headers.update({'Authorization': 'Bearer {0}'.format(self.Key)})
			s.verify = self.verify
			setattr(self, 'Session', s)

		else:
			return('{0} is not a valid "AuthType". Must be "Normal" or "APIKey".'.format(AuthType))

	def CurrentOrganization(self):
		run = self.Session.get('{0}/api/org'.format(self.url))
		return(run.json())

	def OrganizationList(self):
		run = self.Session.get('{0}/api/orgs'.format(self.url))
		return(run.json())

	def OrganizationSearch(self, orgName):
		run = self.Session.get('{0}/api/orgs/name/{1}'.format(self.url, orgName))
		return(run.json())

	def OrganizationCreate(self, orgName):
		json_data = {"name":"{0}".format(orgName)}
		run = self.Session.post('{0}/api/orgs'.format(self.url), data=json_data)
		return(run.json())

	def OrganizationUpdate(self, orgId, orgNewName):
		json_data = {"name":"{0}".format(orgNewName)}
		run = self.Session.put('{0}/api/orgs/{1}'.format(self.url, orgId), data=json_data)
		return(run.json())

	def OrganizationDelete(self, orgId):
		run = self.Session.delete('{0}/api/orgs/{1}'.format(self.url, orgId))
		return(run.json())

	def OrganizationSwitch(self, orgId):
		run = self.Session.post('{0}/api/user/using/{1}'.format(self.url, orgId))	
		return(run.json())

	def DashboardSearch(self, **kwargs):
		url_search = self.url + '/api/search?type=dash-db'
		for key in ('DashboardName', 'Tag', 'Starred'):
			if key in kwargs:
				if key == 'DashboardName':
					url_search = url_search + '&query={0}'.format(kwargs[key])
				if key == 'Tag':
					url_search = url_search + '&tag={0}'.format(kwargs[key])
				if key == 'Starred':
					if type(kwargs[key]) == type(True):
						url_search = url_search + '&starred={0}'.format(str(kwargs[key]).lower())
					else:
						return('Argument "Starred" must be boolean, "True" or "False".')
		run = self.Session.get(url_search)
		return(run.json())

	def DashboardDownload(self, DashboardUid, FileName):
		try:
			data = self.Session.get('{0}/api/dashboards/uid/{1}'.format(self.url, DashboardUid)).json()
			file = open(FileName, 'w')
			file.write(json.dumps(data['dashboard'], indent=2))
			file.close()
		except Exception as e:
			return(e)

	def DashboardUpload(self, FileName, Overwrite=False, FolderId=0):
		with open(FileName) as json_file:
			json_content = json.load(json_file)
		json_content['id'] = 'null'
		json_data = { "folderId": FolderId, "overwrite": Overwrite, "dashboard": json_content }	
		run = self.Session.post('{0}/api/dashboards/db'.format(self.url), json=json_data)
		return(run.json())
