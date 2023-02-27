const App = {
    data() {
        return {
            title: 'Тесты',

            testList: undefined,
            test: undefined,

            access_token: undefined,
            loginOpen: false,
            loginShowPassword: false,
            loginInfo: {
                username: "demo_account",
                password: "qwerty1234",
                //fingerprint: undefined,
            },
            registrationOpen: false,
            registrationShowPassword: false,
            registrationInfo: {
                username: "demo_account",
                password: "qwerty1234",
                name: "default name",
                email: "example@example.com",
            },
        }
    },
    // https://v3.ru.vuejs.org/ru/guide/instance.html#диаграмма-жизненного-цикла
    beforeCreate() {},
    created() {
        // Initialize the agent at application startup.
        const fpPromise = import('https://openfpcdn.io/fingerprintjs/v3')
        .then(FingerprintJS => FingerprintJS.load())

        // Get the visitor identifier when you need it.
        fpPromise
        .then(fp => fp.get())
        .then(result => {
            this.loginInfo.fingerprint = result.visitorId // result.components
            this.refreshToken()
        })
        .catch(error => console.error(error))

        if (location.pathname === '/') {
            this.retrieveAllTests()
        }

        addEventListener('popstate', (event) => { 
            if (location.pathname === '/') {
                this.openTestsList()
            }
        })

        // проверить локально что не закончился JWT токен и если просрочен, то обновить
    },
    beforeMount() {},
    mounted() {},
    beforeUnmount() {},
    unmounted() {},

    beforeUpdate(){},
    updated(){},

    computed: {},
    watch: {},
    methods: {
        page(){
            return location.pathname == '/' ? 'list' : 'test'
        },

        parseJWT (token) {
            const base64Payload = token.split('.')[1]
            const base64 = base64Payload.replace(/-/g, '+').replace(/_/g, '/')
            const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(c => {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
            }).join(''))

            return JSON.parse(jsonPayload)
        },

        refreshToken() {
            fetch('/api/auth/refresh-token', { method: 'POST' })
            .then(response => {
                if (response.ok)
                    response.json().then(json => {
                        this.access_token = `Bearer ${json.access_token}`
                        this.title = "Тесты"
                        history.pushState(null, null, '/')

                        const parsedJWT = this.parseJWT(json.access_token)
                        const expiredAt = new Date(parsedJWT.exp)
                        const now = (new Date()).getTime() / 1000
                        const timeout = (expiredAt - now - 3) * 1000
                        setTimeout(() => {
                            if (this.access_token === `Bearer ${json.access_token}`) {
                                this.refreshToken()
                                /*if (this.access_token === `Bearer ${json.access_token}`) {
                                    this.access_token = null
                                }*/
                            }
                        }, timeout)
                    })
                else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },

        openTestsList() {
            this.title = 'Тесты'
            history.pushState(null, null, '/')
            this.retrieveAllTests()
        },

        signUpOpenForm() {
            this.registrationShowPassword = false
            this.registrationOpen = true
            this.$nextTick(() => {
                this.$refs.reg.focus()
            })
        },

        signInOpenForm() {
            this.loginShowPassword = false
            this.loginOpen = true
            this.$nextTick(() => {
                this.$refs.login.focus()
            })
        },

        signIn() {
            if (this.loginInfo.username == '' || this.loginInfo.password == '') {
                console.log("sign-in: required login and password")
                return
            }

            const URL = '/api/auth/sign-in'
            fetch(URL, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                },
                redirect: 'error',
                body: JSON.stringify({
                    username: this.loginInfo.username,
                    password: this.loginInfo.password
                })
            })
            .then(response => {
                if (response.ok)
                    response.json().then(json => {
                        this.access_token = `Bearer ${json.access_token}`
                        this.loginOpen = false

                        const parsedJWT = this.parseJWT(json.access_token)
                        const expiredAt = new Date(parsedJWT.exp)
                        const now = (new Date()).getTime() / 1000
                        const timeout = (expiredAt - now) * 1000
                        // обнулить просроченный токен
                        setTimeout(() => {
                            if (this.access_token === `Bearer ${json.access_token}`) {
                                this.access_token = null
                                //this.refreshToken()
                            }
                        }, timeout)
                    })
                else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },

        signUp() {
            if (this.registrationInfo.username == '' || this.registrationInfo.password == '' || this.registrationInfo.email == '') {
                console.log("error")
                return
            }

            const URL = '/api/auth/sign-up'
            fetch(URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                redirect: 'error',
                body: JSON.stringify(this.registrationInfo)
            })
            .then(response => {
                if (response.ok) {
                    this.registrationOpen = false
                    this.loginOpen = true
                }
                else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },

        signOut() {
            fetch('/api/auth/sign-out', { method: 'POST'})
            .then(response => {
                if (response.ok) {
                    this.retrieveAllTests()
                    this.access_token = undefined
                    this.title = 'Тесты'
                    history.pushState(null, null, '/')
                } else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },

        retrieveAllTests() {
            fetch('/api/test', { method: 'GET'})
            .then(response => {
                if (response.ok)
                    response.json().then(json => {
                        this.testList = json
                        this.test = undefined
                        this.title = 'Тесты'
                    })
                else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },

        retrieveTestById(test_id) {
            if (!this.access_token) {
                this.signInOpenForm()
                return
            }

            (async () => {
                const testDataPromise = fetch(`/api/test/${test_id}`)
                const questionsDataPromise = fetch(`/api/question-answer?test_id=${test_id}`)
                const answersDataPromise = fetch(`/api/question?test_id=${test_id}`)

                const [testDataRes, answersDataRes, questionsDataRes] = await Promise.all([
                    testDataPromise,
                    questionsDataPromise,
                    answersDataPromise
                ]);
                if (!testDataRes.ok || !answersDataRes.ok || !questionsDataRes.ok) {
                    return
                }

                test = {}
                test.test = await testDataRes.json()
                test.answers = await answersDataRes.json()
                test.questions = await questionsDataRes.json()
                test.completed = test.questions.length === 0 || 'true_answers' in test.questions[0] // костыль

                for (let i = 0; i < test.questions.length; i++) {
                    let question = test.questions[i]
                    if (question.answer_type === 'many_select') {
                        question.response = []
                    }

                    for (let j = 0; j < test.answers.length; j++) {
                        let answer = test.answers[j]
                        if (question.id === answer.question_id && 0 < answer.answer.length) {
                            question.response = question.answer_type === 'many_select' ? answer.answer : answer.answer[0]
                        }
                    }

                    // true_answers подсветить зелёным
                    for (let j = 0; j < question.show_answers.length; j++) {
                        question.show_answers[j] = {
                            value: question.show_answers[j],
                            style: question.true_answers && question.true_answers.includes(question.show_answers[j]) ? { color: "green" } : {}
                        }
                    }
                    //if (question.answer_type === 'freeField') {}
                }
                return test
            })()
            .then(response => {
                if (response) {
                    this.test = response
                    this.testList = undefined
                    this.title = this.test.test.title
                    if (location.pathname == '/')
                        history.pushState(null, null, 'test/' + test_id)
                }
            })
        },

        setAnswer(event) {
            if (!this.access_token) {
                signInOpenForm()
                return
            }

            const question_index = Number(event.target.getAttribute('question_index'))
            const question = this.test.questions[question_index]

            if (!question.response || question.response == '' || question.response.length === 0) {
                console.log('empty answer')
                return
            }

            const URL = '/api/question-answer'
            fetch(URL, {
                method: 'POST',
                headers: {
                    'Authorization': this.access_token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "question_id": question.id,
                    "answer": question.answer_type === 'many_select' ? question.response : [question.response],
                })
            })
            .then(response => {
                if (response.ok)
                    response.json().then(json => {
                        console.log(json)
                    })
                else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },

        completeTest(test_id) {
            if (!this.access_token) {
                this.signInOpenForm()
                return
            }

            const URL = `/api/completed-test`
            fetch(URL, {
                method: 'POST',
                headers: {
                    'Authorization': this.access_token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "test_id": test_id
                })
            })
            .then(response => {
                if (response.ok)
                    this.retrieveTestById(test_id)
                else
                    console.log(response)
            })
            .catch(err => console.log(err))
        },
    },
}

Vue.createApp(App).mount('#vue-app')
