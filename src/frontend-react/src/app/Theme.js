import {
    createMuiTheme,
} from '@material-ui/core';

const Theme = createMuiTheme({
    palette: {
        type: 'light',
        primary: {
            // light: will be calculated from palette.primary.main,
            main: '#b20fb8',
            // dark: will be calculated from palette.primary.main,
            // contrastText: will be calculated to contrast with palette.primary.main
        },
        secondary: {
            light: '#0066ff',
            main: '#b20fb8',
            // dark: will be calculated from palette.secondary.main,
            contrastText: '#ffffff',
        },
        // error: will use the default color
        info: {
            light: '#b20fb8',
            main: '#b20fb8',
            // dark: will be calculated from palette.secondary.main,
            contrastText: '#ffffff',
        },
    },
    typography: {
        useNextVariants: true,
        h6: {
            color: "#b20fb8",
            fontSize: "1.1rem",
            fontFamily: "Roboto, Helvetica, Arial, sans-serif",
            fontWeight: 800
        },
        h5: {
            color: "#084081",
            fontSize: "1.2rem",
            fontFamily: "Roboto, Helvetica, Arial, sans-serif",
            fontWeight: 800
        },
        h4: {
            color: "#b20fb8",
            fontSize: "1.8rem",
            fontFamily: "Roboto, Helvetica, Arial, sans-serif",
            fontWeight: 900
        },
    },
    overrides: {
        MuiOutlinedInput: {
            root: {
                backgroundColor: "#ffffff",
                position: "relative",
                borderRadius: "4px",
            }
        },
    }
});

export default Theme;