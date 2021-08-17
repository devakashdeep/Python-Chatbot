
const headerHeight = document.querySelector('header').clientHeight;
const screenHeight = `${window.screen.height - 2.4 * headerHeight}px`;
// const banner = document.querySelector('.banner');
// banner.style.height = screenHeight;
// console.log(banner);

const openSidebar = document.querySelector('#open-sidebar')
const closeSidebar = document.querySelector('#close-sidebar')
const sidebar = document.querySelector('#sidebar')
openSidebar.addEventListener('click', () => {
    sidebar.style.display = 'block';
})
closeSidebar.addEventListener('click', () => {
    sidebar.style.display = 'none';
})
$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1
        }
    }
})
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const sendMessage = () => {
    const msg = document.querySelector('#ask').value
    const msgsection = document.querySelector('#msg-section')
    const htmlSender = `<div class="msg-sender">
    <p>${msg}</p>
    <p style="font-size:12px; color:#121212">${new Date(Date.now()).toTimeString()} user</p>
    </div>`
    msgsection.insertAdjacentHTML('beforeend', htmlSender);
    var myHeaders = new Headers();
    const csrftoken = getCookie('csrftoken');

    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("X-CSRFToken", csrftoken)
    var raw = JSON.stringify({
        ask: msg
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,

    };

    fetch("/chat-bot/", requestOptions)
        .then(response => response.json())
        .then(result => {
            const html = `<div class="msg-recieved">
            <p>${result.result}</p>
            <p style="font-size:12px; color:#121212">${new Date(Date.now()).toTimeString()} chat bot</p>
            </div>`
            msgsection.insertAdjacentHTML('beforeend', html);
            msg = ""

        })
        .catch(error => console.log('error', error));
}

const sendMessageBTN = document.querySelector('#sendMessage')
document.querySelector('#ask').addEventListener('keypress', (e) => {
    if (e.key == 'Enter') {
        if (document.querySelector('#ask').value !== '') {
            sendMessage()
        }
    }
})
sendMessageBTN.addEventListener('click', sendMessage)

const stringToArray = (str) => {
    if (str) {
        return str.split('|')
    }
}

const arrayToString = (arr) => {
    return arr.toString();
}

const setSessioValToHTML = (id, key) => {
    const data = sessionStorage.getItem(key);
    const arr = stringToArray(data);
    let htmlTags = '';
    if (arr) {
        arr.map((item) => {
            htmlTags += `<span class="items-pills-${key.split('@')[1]}">${item}</span>`;
        });
    }
    // console.log(arr);
    const html = document.querySelector(id);
    html.innerHTML = htmlTags;
}

setSessioValToHTML('#patternsa', '@patterns');
setSessioValToHTML('#responses_u', '@responses');

const patterns_pills = document.querySelectorAll('.items-pills-patterns');
const responses_pills = document.querySelectorAll('.items-pills-responses');

if (patterns_pills && patterns_pills.length > 0) {
    patterns_pills.forEach((item) => {
        item.addEventListener('click', () => {
            let val = item.textContent;
            const data = sessionStorage.getItem('@patterns');
            const arr = stringToArray(data);
            const result = arr.filter(i => i !== val);
            let strData = ''
            if (result) {
                for (let i = 0; i < result.length; i++) {
                    strData += result[i];
                    if (i < result.length - 1) {
                        strData += '|'
                    }
                }
            }
            sessionStorage.setItem('@patterns', strData.toString());
            setSessioValToHTML('#patternsa', '@patterns');
        })
    })
}
if (responses_pills && responses_pills.length > 0) {
    responses_pills.forEach((item) => {
        item.addEventListener('click', () => {
            let val = item.textContent;
            const data = sessionStorage.getItem('@responses');
            const arr = stringToArray(data);
            const result = arr.filter(i => i !== val);
            let strData = ''
            if (result) {
                for (let i = 0; i < result.length; i++) {
                    strData += result[i];
                    if (i < result.length - 1) {
                        strData += '|'
                    }
                }
            }
            sessionStorage.setItem('@responses', strData.toString());
            setSessioValToHTML('#responses_u', '@responses');
        })
    })
}
const patterns = document.querySelector('#patterns')
patterns.addEventListener('keypress', (e) => {
    console.log(e.key)
    if (e.key == 'Enter' || e.key == "|" || patterns.value.includes('|')) {
        const ses_patterns = sessionStorage.getItem('@patterns');
        const a_val = patterns.value.split('|')[0];
        if (a_val != '') {
            if (ses_patterns && (ses_patterns !== null || ses_patterns !== undefined)) {
                let data = ses_patterns;
                const a_val = patterns.value.split('|')[0];
                sessionStorage.setItem('@patterns', (data + '|' + a_val).toString())
            } else {
                const a_val = patterns.value.split('|')[0];
                sessionStorage.setItem('@patterns', a_val.toString())
            }
            setSessioValToHTML('#patternsa', '@patterns');
            patterns.value = '';
        }
        patterns.value = '';
    }
})
patterns.addEventListener('input', (e) => {
    console.log(e.key)
    if (patterns.value.includes('|')) {
        const ses_patterns = sessionStorage.getItem('@patterns');
        const a_val = patterns.value.split('|')[0];
        if (a_val != '') {
            if (ses_patterns && (ses_patterns !== null || ses_patterns !== undefined)) {
                let data = ses_patterns;
                const a_val = patterns.value.split('|')[0];
                sessionStorage.setItem('@patterns', (data + '|' + a_val).toString())
            } else {
                const a_val = patterns.value.split('|')[0];
                sessionStorage.setItem('@patterns', a_val.toString())
            }
            setSessioValToHTML('#patternsa', '@patterns');
            patterns.value = '';
        }
        patterns.value = '';
    }
})

const responses = document.querySelector('#responses')
responses.addEventListener('input', (e) => {

    if (responses.value.includes('|')) {
        const ses_responses = sessionStorage.getItem('@responses');
        const a_val = responses.value.split('|')[0];
        if (a_val != '') {
            if (ses_responses && (ses_responses !== null || ses_responses !== undefined)) {
                let data = ses_responses;
                const a_val = responses.value.split('|')[0];
                sessionStorage.setItem('@responses', (data + '|' + a_val).toString())
            } else {
                const a_val = responses.value.split('|')[0];
                sessionStorage.setItem('@responses', a_val.toString())
            }
            setSessioValToHTML('#responses_u', '@responses');
            responses.value = '';
        }
        responses.value = '';
    }
})
responses.addEventListener('keypress', (e) => {

    if (e.key == 'Enter' || e.key == "|" || responses.value.includes('|')) {
        const ses_responses = sessionStorage.getItem('@responses');
        const a_val = responses.value.split('|')[0];
        if (a_val != '') {
            if (ses_responses && (ses_responses !== null || ses_responses !== undefined)) {
                let data = ses_responses;
                const a_val = responses.value.split('|')[0];
                sessionStorage.setItem('@responses', (data + '|' + a_val).toString())
            } else {
                const a_val = responses.value.split('|')[0];
                sessionStorage.setItem('@responses', a_val.toString())
            }
            setSessioValToHTML('#responses_u', '@responses');
            responses.value = '';
        }
    }
})


const submitIntents = () => {
    const csrftoken = getCookie('csrftoken');

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append('X-CSRFToken', csrftoken);
    const tag = document.querySelector('#tagsIn').value;
    const patterns = sessionStorage.getItem('@patterns').split('|');
    const responses = sessionStorage.getItem('@responses').split('|');
    var raw = JSON.stringify({
        tag: tag,
        patterns: patterns,
        responses: responses
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
    };

    const clearIntents = () => {
        sessionStorage.clear();

        setSessioValToHTML('#patternsa', '@patterns');
        setSessioValToHTML('#responses_u', '@responses');

        // console.log(arr);
    }

    fetch("/intents/", requestOptions)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            const intentList = document.querySelector('#intentList')
            let html = '';
            result.result.map((item) => {
                html += `<li class="mb-2">${item.tag}</li>`
            })
            intentList.innerHTML = html;
            clearIntents()
        })
        .catch(error => console.log('error', error));
}

const saveIntent = document.querySelector('#submit-intents');
saveIntent.addEventListener('click', submitIntents);




const dropdownMenuButton = document.querySelector('#dropdownMenuButton');
dropdownMenuButton.addEventListener('click', function () {
    const dropdownMenuTop = document.querySelectorAll('.dropdown-menu')
    dropdownMenuTop.forEach((item) => {
        if (item.getAttribute('aria-labelledby') === 'dropdownMenuButton') {
            const claList = item.classList
            claList.toggle('showMenu')
        }
    })
})
//--></script>



