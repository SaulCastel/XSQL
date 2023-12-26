import axios from "axios";

//Conexión con API
const apiURL = "http://127.0.0.1:8000/";

//Obtener data de salida
export const getOutput = async(data) => {
    try{
        return await axios.get(apiURL+'getData',data)
    }catch(err){
        throw err
    }
}

//Enviar entrada
export const setInput = async(data) => {
    console.log(data)
    try{
        return await axios.post(apiURL+'interpret',data)
    }catch(err){
        throw err;
    }
}