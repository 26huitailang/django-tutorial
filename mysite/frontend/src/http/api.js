// export function apiBase() {
//   let hostname = window.location.hostname;
//   let API_BASE_URL = 'http://localhost:8000';  //默认环境
//   if (hostname === 'production.com') {  //正式环境
//     API_BASE_URL = 'http://production.com';
//   } else if (hostname === 'test.production.com') {  //公网测试环境
//     API_BASE_URL = 'http://test.production.com';
//   } else if (hostname === 'develop.com') {  //内网测试环境
//     API_BASE_URL = 'http://develop.com';
//   }
//   return API_BASE_URL;
// }
export function apiBase() {
  return process.env.VUE_APP_API_ROOT;
}

export function wsBase() {
  return process.env.VUE_APP_WS_ROOT;
}

export function apiV1() {
  return apiBase() + "/api/v1";
}

export function AUTH() {
  return {
    TokenAuth: apiBase() + "/api-token-auth/",
    Login: apiV1() + "/auth/login/",
    Logout: apiV1() + "/auth/logout/"
  };
}

export function MZITU(id, page, page_size, search) {
  return {
    SuitesDownload: apiV1() + "/mzitu/suites/download/?suite_url=",
    ThemesDownload: apiV1() + "/mzitu/themes/download/?theme_url=",
    SuitesList: apiV1() + `/mzitu/suites/?page=${page}&page_siez=${page_size}&search=${search}`,
    SuitesDetail: apiV1() + `/mzitu/suites/${id}/`,
    // SuitesDetail: this.SuitesList + `${id}`,
    Tags: apiV1() + "/mzitu/tags/",
    TagDelete: apiV1() + `/mzitu/tags/${id}/`
  };
}

export function CHART() {
  return {
    TagsBar: apiV1() + "/mzitu/charts/tags_bar/",
    ProxyIpsBar: apiV1() + "/mzitu/charts/proxyips_bar/",
  }
}
