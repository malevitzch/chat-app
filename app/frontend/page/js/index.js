//setup
const MAX_MESSAGES = 3

list = document.getElementById('msgList');
for(let i = 0; i < MAX_MESSAGES; i++) {
    var li = document.createElement('li');
    list.appendChild(li);
}


//initializing the socket
const socket = io('/socket.io');

socket.on('update', (data) => {
    jdata = data.json();
    const items = list.getElementsByTagName('li');
    for (let i = 0; i < jdata.length; i++) 
    {
	items[i].textContent = jdata[i];
    }
});

function post() {
    const msg = document.getElementById('messageform').value;
    socket.emit('post', msg);
    console.log("POSTED MSG");
}

socket.emit('get');
/*
async function setup() {
    let req;
    await fetch('/api/get')
	.then(response => response.json())
	.then(data => req = data);
    const items = list.getElementsByTagName('li');
    for (let i = 0; i < req.length; i++) 
    {
	items[i].textContent = req[i];
    }
}

async function post(event)
{
    const inputString = document.getElementById('messageform').value;

    await fetch('/api/post/' + inputString)
	.then(response => response.json());
    console.log('Submitted value:', inputValue);
    setup();
}

setInterval(async () => {setup()}, 500);*/
