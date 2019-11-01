const basic = {
    backend: 'http://182.92.119.20',
    // backend: 'http://localhost:8000',
    search: '/api/search',
    changePasswd: '/api/changePasswd',
    uploadArticle: '/api/uploadArticle',
    uploadJournal: '/api/uploadJournal',
    modifyArticle: '/api/modifyArticle',
    deleteArticle: '/api/deleteArticle',
    requestContent: '/api/requestContent',
    login: '/api/login'
}

export default {
    backend: basic.backend,
    search: basic.backend + basic.search,
    changePasswd: basic.backend + basic.changePasswd,
    uploadArticle: basic.backend + basic.uploadArticle,
    uploadJournal: basic.backend + basic.uploadJournal,
    modifyArticle: basic.backend + basic.modifyArticle,
    deleteArticle: basic.backend + basic.deleteArticle,
    requestContent: basic.backend + basic.requestContent,
    login: basic.backend + basic.login
}