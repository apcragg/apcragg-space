export function load_plot() {
    var plot = new sigplot.Plot(document.getElementById("plot"), {});
    var data = [];
    var npts = 1024;
    for (var ii = 0; ii < npts; ++ii) {
    data.push(Math.sin(ii * 2 * Math.PI *7.34 / npts));
    }
    plot.overlay_array(data);
}
