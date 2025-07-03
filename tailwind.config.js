const kutty = require("kutty");
const daisyui = require("daisyui");

module.exports = {
    content: ['./app/**/*.py', './app/**/*.html'],
    theme: {
        extend: {
            colors: {
                primary: {
                    light: "#a9b4a6",
                    default: "#6F826A",
                    dark: "#434e40",
                },
                secondary: {
                    light: "#d9bea2",
                    default: "#BF9264",
                    dark: "#73583c",
                },
                tertiary: {
                    dark: "#708262",
                    default: "#BBD8A3",
                    light: "#d6e8c8",
                },
                quaternary: {
                    light: "#f6f7dc",
                    default: "#F0F1C5",
                    dark: "#909176",
                },
            },
        },
    },
    fontFamily: {
        sans: ['Graphik', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
    },
    extend: {
        spacing: {
            '8xl': '96rem',
            '9xl': '128rem',
        },
        borderRadius: {
            '4xl': '2rem',
        }
    },
    plugins: [daisyui],
}
