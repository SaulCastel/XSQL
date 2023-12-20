import axios from "axios";

//Conexión con API
const apiURL = ""

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
    try{
        return await axios.post(apiURL+'setData',data)
    }catch(err){
        throw err;
    }
}