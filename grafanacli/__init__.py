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

	def OrganizationGetUsers(self, orgId):
		run = self.Session.get('{0}/api/orgs/{1}/users'.format(self.url, orgId))	
		return(run.json())

	def OrganizationAddUser(self, orgId, loginOrEmail, role):
		json_data = {"loginOrEmail":"{0}".format(loginOrEmail), "role":"{0}".format(role)}
		run = self.Session.post('{0}/api/orgs/{1}/users'.format(self.url, orgId), json=json_data)	
		return(run.json())

	def OrganizationUpdateUser(self, orgId, userId, role):
		json_data = {"role":"{0}".format(role)}
		run = self.Session.patch('{0}/api/orgs/{1}/users/{2}'.format(self.url, orgId, userId), data=json_data)	
		return(run.json())

	def OrganizationDeleteUser(self, orgId, userId):
		run = self.Session.delete('{0}/api/orgs/{1}/users/{2}'.format(self.url, orgId, userId))	
		return(run.json())

	def OrganizationGetPreferences(self):
		run = self.Session.get('{0}/api/org/preferences'.format(self.url))
		return(run.json())

	def OrganizationUpdatePreferences(self, **kwargs):
		json_data = {}
		for key in ('theme', 'homeDashboardId', 'timezone'):
			if key in kwargs:
				if key == 'theme':
					json_data['theme'] = kwargs[key]
				if key == 'homeDashboardId':
					json_data['homeDashboardId'] = kwargs[key]
				if key == 'timezone':
					json_data['timezone'] = kwargs[key]
		run = self.Session.put('{0}/api/org/preferences'.format(self.url), json=json_data)
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

	def DashboardGet(self, DashboardUid):
		run = self.Session.get('{0}/api/dashboards/uid/{1}'.format(self.url, DashboardUid))
		return(run.json())

	def DashboardDelete(self, DashboardUid):
		run = self.Session.delete('{0}/api/dashboards/uid/{1}'.format(self.url, DashboardUid))
		return(run.json())

	def DashboardHome(self):
		run = self.Session.get('{0}/api/dashboards/home'.format(self.url))
		return(run.json())

	def DashboardTags(self):
		run = self.Session.get('{0}/api/dashboards/tags'.format(self.url))
		return(run.json())
		
	def GlobalUserAdd(self, name, email, login, password):
		json_data = {"name":"{0}".format(name), 
						"email":"{0}".format(email),
						"login":"{0}".format(login),
						"password":"{0}".format(password)}
		run = self.Session.post('{0}/api/admin/users'.format(self.url), json=json_data)
		return(run.json())

	def GlobalUserUpdatePassword(self, userId, newPassword):
		json_data = {"password":"{0}".format(newPassword)}
		run = self.Session.put('{0}/api/admin/users/{1}/password'.format(self.url, userId), json=json_data)
		return(run.json())

	def GlobalUserGrafanaAdmin(self, userId, grafanaAdmin=False):
		json_data = {"isGrafanaAdmin":grafanaAdmin}
		run = self.Session.put('{0}/api/admin/users/{1}/permissions'.format(self.url, userId), json=json_data)
		return(run.json())

	def GlobalUserDelete(self, userId):
		run = self.Session.delete('{0}/api/admin/users/{1}'.format(self.url, userId))
		return(run.json())

	def GlobalUserList(self):
		run = self.Session.get('{0}/api/users'.format(self.url))
		return(run.json())

	def GlobalUserSearch(self, loginOrEmail):
		run = self.Session.get('{0}/api/users/lookup?loginOrEmail={1}'.format(self.url, loginOrEmail))
		return(run.json())

	def DatasourceList(self):
		run = self.Session.get('{0}/api/datasources'.format(self.url))
		return(run.json())

	def DatasourceGet(self, dsId):
		run = self.Session.get('{0}/api/datasources/{1}'.format(self.url, dsId))
		return(run.json())

	def DatasourceCreate(self, ds_json):
		run = self.Session.post('{0}/api/datasources'.format(self.url), json=ds_json)
		return(run.json())	

	def DatasourceUpdate(self, dsId, ds_json):
		run = self.Session.put('{0}/api/datasources/{1}'.format(self.url, dsId), json=ds_json)
		return(run.json())

	def DatasourceDelete(self, dsId):
		run = self.Session.delete('{0}/api/datasources/{1}'.format(self.url, dsId))
		return(run.json())

	def ZabbixPlugin(self, Enabled=True):
		json_data = {'id': 'alexanderzobnin-zabbix-app', 'enabled': Enabled}
		run = self.Session.post('{0}/api/plugins/alexanderzobnin-zabbix-app/settings'.format(self.url), json=json_data)
		return(run.json())