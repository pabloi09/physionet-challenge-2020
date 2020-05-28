import React, { useState } from 'react';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import UploadPage from "./UploadPage" 
//import DiagnosisPage from "./DiagnosisPage" 
import {dark,light} from "./assets/themes"
import LegendWrapper from "./LegendWrapper"
import heatmap from "./assets/heatmap"

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
    var response = await fetch("https://www.tfg-ecg.duckdns.org/classifier",{
                      method:'POST',
                      body: formData,
                    })
    console.log("Respondido")
    //response = await response.json()
    //response.heatmap = heatmap
    //setDiagnosis(response)
  }
  return (
    <ThemeProvider theme = {theme}>
        <LegendWrapper setDarkTheme={setDarkTheme}
                       darkTheme={darkTheme}/>
        {diagnosis.leads ? 
          <DiagnosisPage diagnosis={diagnosis}/>:
          <UploadPage setFiles={setFiles} 
                      filesUpload={filesUpload}/>}
    </ThemeProvider>
  );
}

export default App;