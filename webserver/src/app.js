import { sleep_ms } from './utils';

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

async function get_usage(){
    const response = await fetch('/api/cpu/usage');
    const data = await response.json();
    return data['usage'];
}

async function get_capture_time(){
    const response = await fetch('/api/sdr/capture_time');
    const data = await response.json();
    const t_ms = Math.round(data['capture_t'] * 1e4) / 10;
    return t_ms;
}

export async function run_app(){
    while(true){
        data = await get_usage()
        setElementString('rpi_usage', data)

        data = await get_capture_time()
        setElementString('capture_t', data)
        await sleep_ms(500);
    }
}
