import { sleep_ms } from "./utils";
var gaussian = require('gaussian')

function load_plot(plot_id, npts) {
    var plot_options = {
        autohide_panbars: true,
        hide_note: false,
        ymin:10,
        ymax:-50,
        xlabel: "Time",
    };

    var plot = new sigplot.Plot(document.getElementById(plot_id), plot_options);

    let data_header = {
        xunits: "us",
    };

    let layer_options = {
        legend: true,
        color: "green",
    };

    let layer = plot.overlay_array(null, data_header, layer_options);
    return {plot: plot, layer: layer};
}

export async function run_plot(id, n_plots, npts = 1024) {
    let plots = []
    for (let i = 1; i <= n_plots; i++){
        plots.push(load_plot(id + i, npts))
    }

    while(true) {
        const resp = await fetch('/api/sdr/spectrum?n=' + n_plots);
        const data_resp = await resp.json();
        let spectrum = data_resp['spectrum']
        for (let i = 0; i < n_plots; i++){
            let data = spectrum[i]
            let plot = plots[i]['plot']
            let layer = plots[i]['layer']
            plot.reload(layer, data)
        }
        await sleep_ms(1000 / 60);
    }
}
