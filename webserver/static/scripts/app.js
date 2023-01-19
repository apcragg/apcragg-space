import { load_plot } from './plot.js';

function date(){
    const d = new Date();
    let time = d.toLocaleString("en-US", {timeZoneName: 'short'})
    let local_t = document.getElementById("local_t");
    local_t.innerHTML = String(time);

    let time_mt = time = d.toLocaleString("en-US", {timeZone: 'America/Denver', timeZoneName: 'short'})
    let mt_t = document.getElementById("mt_t");
    mt_t.innerHTML = String(time_mt);
}

setInterval(date, 100);

function setElementString(id, str){
    let element = document.getElementById(id);
    element.innerHTML = str
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function get_usage(){
    const response = await fetch('/api/cpu/usage');
    const data = await response.json();
    return data['usage'];
}

async function get_temp(){
    const response = await fetch('/api/cpu/temp');
    const data = await response.json();
    return data['temp0'];
}

async function run(){
    while(true){
        let data = await get_temp()
        setElementString('rpi_t', data)

        data = await get_usage()
        setElementString('rpi_usage', data)
        await sleep(500);
    }
}



run();
load_plot();
