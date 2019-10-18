const basic = {
    backend: 'http://localhost:8000',
    search: '/search'
}

export default {
    backend: basic.backend,
    search: basic.backend + basic.search
}