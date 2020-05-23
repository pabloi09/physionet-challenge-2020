import React from 'react';
import ProbabilitiesComponent from "./ProbabilitiesComponent"
import { Typography } from '@material-ui/core';
import {Paper} from "@material-ui/core"
import ConfusionMatrixComponent from "./ConfusionMatrixComponent"

function ModelPart(props) {

    
    return (
        <Paper style={{borderRadius:"10px", paddingTop:"10px", paddingBottom:"10px", height:"100%"}}>
            <Typography variant="h3" style={{margin:"10px"}}>Diagnóstico</Typography>
            <Typography style={{margin:"10px"}}>
                El modelo calcula como mas probable que el electrocardiograma pertenzca a una
                persona con <b>{props.diagnosis.classes
                            .filter((c,i)=>props.diagnosis.labels[i] === 1)
                            .reduce((acc="" ,val)=>(acc + val + " y ") )}</b>
            </Typography>
            <ProbabilitiesComponent diagnosis={props.diagnosis}/>
            <Typography style={{margin:"10px"}}>
                A continuación, se muestra el comportamiento del modelo empleado a la hora de diagnosticar cada enfermedad para el conjunto de datos utilizado.
            </Typography>
            <ConfusionMatrixComponent diagnosis={props.diagnosis}/>
        </Paper>
    );
}

export default ModelPart;