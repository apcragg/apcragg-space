import * as bootstrap from 'bootstrap';
import '../static/css/styles.scss';
import '../static/css/stylesheet.css';
import { run_app } from "./app";
import { run_plot } from "./plot";

run_plot('plot', 6);
run_app();
