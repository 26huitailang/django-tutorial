export function apiBase() {
  let hostname = window.location.hostname;
  let API_BASE_URL = 'http://localhost:8000';  //默认环境
  if (hostname === 'production.com') {  //正式环境
    API_BASE_URL = 'http://production.com';
  } else if (hostname === 'test.production.com') {  //公网测试环境
    API_BASE_URL = 'http://test.production.com';
  } else if (hostname === 'develop.com') {  //内网测试环境
    API_BASE_URL = 'http://develop.com';
  }
  return API_BASE_URL;
}

export function apiV1() {
  return apiBase() + '/api/v1'
}

export function MZITU (id) {
  return {
    SuitesList: apiV1() + '/mzitu/suites/',
    SuitesDetail: apiV1() + `/mzitu/suites/${id}`,
    // SuitesDetail: this.SuitesList + `${id}`,
    Tags: apiV1() + '/mzitu/tags/',
  }
}