const { NONAME } = require("dns")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const path = require("path")

module.exports = {
    mode: "production",
    entry: "./src/index.js",
    output: {
        filename: "main.[contenthash].js",
        path: path.resolve(__dirname, 'dist'),
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./static/templates/index_template.html",
            minify: {
                collapseWhitespace: false,
                preserveLineBreaks: true,
            },
        })
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                // Loads in reverse order, need to load css first
                use: ["style-loader", "css-loader"],
            }
        ]
    }
}
