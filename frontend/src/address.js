const basic = {
    backend: 'http://localhost:8000',
    search: '/api/search',
    changePasswd: '/api/changePasswd'
}

export default {
    backend: basic.backend,
    search: basic.backend + basic.search,
    changePasswd: basic.backend + basic.changePasswd
}