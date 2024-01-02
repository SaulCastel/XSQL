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
    try{
        return await axios.post(apiURL+'interpret',data)
    }catch(err){
        throw err;
    }
}

// Solicitar EXPORT
export const getExport = async(data) => {
    try{
        return await axios.get(apiURL+'export', data)
    }catch(err){
        throw err;
    }
}

// Solicitar DUMP
export const getDump = async(data) => {
    try{
        return await axios.get(apiURL+'dump', data)
    }catch(err){
        throw err;
    }
}

// Solicitar BASES
export const getBases = async(data) => {
    try{
        return await axios.get(apiURL+'bases', data)
    }catch(err){
        throw err;
    }
}