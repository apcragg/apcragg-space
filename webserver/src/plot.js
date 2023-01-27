import { sleep_ms } from "./utils";
const plot_utils = require('./plot_utils')

function load_plot(plot_id) {
    // Plot-wide settings
    var plot_options = {
        autohide_panbars: true,
        hide_note: false,
        ymin:10,
        ymax:-50,
        xlabel: "Time",
        legend: true,
    };

    var plot = new sigplot.Plot(document.getElementById(plot_id), plot_options);

    // Plot units, note that scaling is applied to data
    let data_header = {
        yunits: "dBm/Hz",
        xunits: "Mhz",
    };

    // Primary trace
    let layer_options = {
        legend: true,
        color: "rgb(20,199,193)",
        fillStyle: ["rgba(0,0,0,0)", "rgb(20,199,193,0.5)"],
        name: 'Plot ' + plot_id.split("plot")[1]
    };

    // Max hold trace
    let max_layer_options = {
        legend: true,
        color: "rgba(228,87,46, .75)",
        name: 'Plot ' + plot_id.split("plot")[1] + " Max",
    };

    // Percentile trace
    let perc_layer_options = {
        legend: true,
        color: "rgba(243,167,18, .75)",
        name: 'Plot ' + plot_id.split("plot")[1] + " Bounds",
    };


    let perc_layer = plot.overlay_array(null, data_header, perc_layer_options);
    let max_layer = plot.overlay_array(null, data_header, max_layer_options);
    let layer = plot.overlay_array(null, data_header, layer_options);
    return {plot: plot, layer: layer, max_layer: max_layer, perc_layer: perc_layer};
}

export async function run_plot(id, n_plots) {
    let plots = []
    for (let i = 1; i <= n_plots; i++){
        plots.push(load_plot(id + i))
    }

    let percentiles = []
    let max_trace = []
    for (let i = 0; i < n_plots; i++){
        max_trace.push([]);
        percentiles.push(new plot_utils.PercentileBounds(100));
    }

    while(true) {
        const resp = await fetch('/api/sdr/spectrum?n=' + n_plots);
        const data_resp = await resp.json();
        let spectrum = data_resp['spectrum']
        for (let i = 0; i < n_plots; i++){
            let data = spectrum[i]

            if (max_trace[i].length != data.length){
                max_trace[i]= new Array(data.length).fill(Number.NEGATIVE_INFINITY)
            }
            max_trace[i] = plot_utils.elementwiseMax(data, max_trace[i]);
            percentiles[i].addMeasurement(data);

            let plot = plots[i]['plot'];
            let layer = plots[i]['layer'];
            let perc_bounds = percentiles[i].getBounds(.95);
            plot.reload(layer, data);
            plot.reload(plots[i]['max_layer'], perc_bounds.map((val, idx) => val[1]));
            plot.reload(plots[i]['perc_layer'], perc_bounds.map((val, idx) => val[0]));
        }
        await sleep_ms(1000 / 15);
    }
}
