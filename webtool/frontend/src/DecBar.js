import React from 'react';
import Brightness4Icon from '@material-ui/icons/Brightness4';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import { AppBar, Toolbar, IconButton, Typography, Link, Tooltip, Dialog, ListItem, List } from "@material-ui/core"
import { makeStyles } from '@material-ui/core/styles';
import { withTheme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    bar: {
        backgroundColor:theme.appbar
    }
  }));
function DecBar(props) {
    const classes = useStyles();

    return (
        <AppBar position="fixed" className={classes.bar}>
          <Toolbar style={{display:"flex", flexDirection:"row", justifyContent:"space-between"}}>
            <Typography variant="h6" >
              <Link href="/" color="inherit" style={{textDecoration:"none"}}>
                Diagnóstico de enfermedades cardiovasculares
              </Link>
              </Typography>
            <div>
            <Tooltip title="Leyenda de enfermedades">
                <IconButton
                    edge="end"
                    aria-label="legend"
                    aria-haspopup="true"
                    onClick={()=>props.setOpen(!props.open)}
                    color="inherit">
                    <InfoOutlinedIcon/>
                </IconButton>
              </Tooltip>
              <Tooltip title="Cambiar a modo oscuro/claro">
                <IconButton
                    edge="end"
                    aria-label="darkmode"
                    aria-haspopup="true"
                    onClick={()=>props.setDarkTheme(!props.darkTheme)}
                    color="inherit">
                    <Brightness4Icon/>
                </IconButton>
              </Tooltip>
            </div>
          </Toolbar>
        </AppBar>
    );
}

export default withTheme(DecBar);