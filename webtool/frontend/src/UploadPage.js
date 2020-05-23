import React, {useState} from 'react';
import FilesComponent from "./FilesComponent"
import {Typography,Paper,Button, Container} from "@material-ui/core"
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';
import { withTheme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  wrapper: {
    margin: theme.spacing(1),
    alignSelf:"flex-end"
  },
  buttonProgress: {
    color: "#2196f3",
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  }
}))

function UploadPage(props) {
    const [count, setCount] = useState(0);
    const [loading, setLoading] = React.useState(false);
    const classes = useStyles();
    return (
      <Container style={{padding:"100px", backgroundColor:props.theme.palette.background.default, height:"100vh"}} maxWidth="xl">
        <Paper  style={{borderRadius:"10px", padding:"20px", display:"flex", flexDirection:"column", alignItems:"center",height:"100%", justifyContent:"space-between"}}>
              <Typography variant="h3" color = "textPrimary">
                Arrastre los ficheros del electrocardigrama para iniciar el diagnóstico
              </Typography>
              <FilesComponent 
                setCount={setCount}
                setFiles={props.setFiles}/>
              <div className={classes.wrapper}>
                <Button disabled={count !== 2} 
                        onClick={()=>{
                                  setCount(0)
                                  setLoading(true)
                                  props.filesUpload()}}>
                  Diagnosticar
                </Button>
                {loading && <CircularProgress size={56} className={classes.buttonProgress} />}
              </div>
        </Paper>
      </Container>
    );
}

export default withTheme(UploadPage);