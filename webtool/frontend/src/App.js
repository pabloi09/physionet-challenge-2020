import React, { useState } from 'react';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { AppBar, Toolbar, IconButton, Typography, Link } from "@material-ui/core"
import UploadPage from "./UploadPage" 
import DiagnosisPage from "./DiagnosisPage" 
import {dark,light} from "./assets/themes"
import Brightness4Icon from '@material-ui/icons/Brightness4';

function App() {
  const [files, setFiles] = useState([]);
  const [diagnosis, setDiagnosis] = useState({})
  const [darkTheme, setDarkTheme] = useState(false)
  const theme = createMuiTheme({
    background: 'linear-gradient(45deg, #2196f3 30%, rgb(175, 61, 228) 90%)',
    palette: {
      type: darkTheme? 'dark':'light'
    },
    nivo: darkTheme? dark:light,
    appbar:darkTheme ? "#424242":"#3f51b5"
  });

  const filesUpload = async () => {
    const formData = new FormData()
    var n = 1
    Object.keys(files).forEach((key) => {
      const file = files[key]
      formData.append('file'+n, new Blob([file], { type: file.type }), file.name || 'file')
      n += 1
    })
    var response = await fetch("http://localhost:5000/",{
                      method:'POST',
                      body: formData,
                    })
    response = await response.json()
    var resp = await fetch("assets/heatmap.json")
    resp = await resp.json()
    response.heatmap = resp
    setDiagnosis(response)
  }
  return (
    <ThemeProvider theme = {theme}>
        <AppBar position="absolute" style={{backgroundColor:theme.appbar}}>
          <Toolbar style={{display:"flex", flexDirection:"row", justifyContent:"space-between"}}>
            <Typography variant="h6" >
              <Link href="/" color="inherit" style={{textDecoration:"none"}}>
                Diagnóstico de enfermedades cardiovasculares
              </Link>
              </Typography>
            <IconButton
                edge="end"
                aria-label="darkmode"
                aria-haspopup="true"
                onClick={()=>setDarkTheme(!darkTheme)}
                color="inherit">
                <Brightness4Icon/>
            </IconButton>
          </Toolbar>
        </AppBar>
        {diagnosis.leads ? <DiagnosisPage diagnosis={diagnosis}/>:<UploadPage setFiles={setFiles} filesUpload={filesUpload}/>}
    </ThemeProvider>
  );
}

export default App;