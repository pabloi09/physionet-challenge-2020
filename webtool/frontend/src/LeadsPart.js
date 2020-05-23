import React, {useState, useLayoutEffect} from 'react';
import { Typography } from '@material-ui/core';
import {Paper, Container} from "@material-ui/core"
import LeadComponent from "./LeadComponent"
function LeadsPart(props) {
    const [width, setWidth] = useState( window.innerWidth > 1280 ? 700:400)
    useLayoutEffect(() => {
        function updateSize() {
          setWidth(window.innerWidth > 1280 ? 700:400)
        }
        window.addEventListener('resize', updateSize);
      }, []);
    
      return (
        <Paper style={{borderRadius:"10px", paddingTop:"10px", paddingBottom:"10px", height:"100%"}}>
            <Typography variant="h3" style={{margin:"10px"}}>Derivaciones del electrocardiograma a diagnosticar</Typography>
            <Typography style={{margin:"10px"}}>
                A continuación se ofrece una vista de las derivaciones del electrocardiograma tras ser filtradas.
                Sobre una derivación
            </Typography>
            <ul>
                    <li><Typography>Ctrl+click para hacer zoom in</Typography></li>
                    <li><Typography>Ctrl+Mayús+click para hacer zoom out</Typography></li>
                </ul>
            {
                props.diagnosis.leads.map((lead)=>{
                    return(
                        <Container style={{width: "100%"}} key={lead.name}>
                            <LeadComponent
                                name={lead.name}
                                signal={lead.signal}
                                width={width}
                                fs={props.diagnosis.fs}/>
                        </Container>
                        )})
                        
            }
        </Paper>
    );
}

export default LeadsPart;