import React, { useState } from 'react';
import Editor from '@monaco-editor/react';

function ConsoleIn({ onExecuteQuery }) {
  const [sqlQuery, setSqlQuery] = useState('');
  const [queryResult, setQueryResult] = useState('');

  const handleExecuteQuery = () => {
    // Aquí puedes realizar la lógica de ejecución de la consulta SQL
    // En este ejemplo, simplemente mostramos datos quemados
    const data = [
      { NOMBRE: 'Juan', ID: 1, DOMICILIO: 'Calle A' },
      { NOMBRE: 'Maria', ID: 2, DOMICILIO: 'Calle B' },
      // Agrega más datos según sea necesario
    ];

    // Obtén los valores entre SELECT y FROM usando una expresión regular
    const match = sqlQuery.match(/SELECT\s+(.*?)\s+FROM/i);
    const selectedFields = match ? match[1].trim() : '';

    // Si no se encontraron campos seleccionados, mostrar un mensaje
    if (!selectedFields) {
      setQueryResult('No se encontraron campos seleccionados');
      return;
    }

    // Construir la salida de la consulta en forma de tabla
    const headers = selectedFields.split(',').map((field) => field.trim());
    const rows = data.map((row) => headers.map((header) => row[header]));

    // Calcular el tamaño de cada celda
    const columnSizes = headers.reduce((sizes, header, columnIndex) => {
      const maxContentLength = Math.max(
        header.length,
        ...rows.map((row) => (`${row[columnIndex]}`.trim() !== '') ? `${row[columnIndex]}`.length : 0)
      );
      sizes[columnIndex] = maxContentLength + 2; // Tamaño fijo de 2 caracteres adicionales
      return sizes;
    }, {});

    const formattedTable = `${generateTableLine(columnSizes, 'top')}
${generateTableRow(headers, columnSizes)}
${generateTableLine(columnSizes, 'middle')}
${rows.map((row) => generateTableRow(row, columnSizes)).join('\n')}
${generateTableLine(columnSizes, 'bottom')}`;

    setQueryResult(formattedTable);
  };

  // Generar una línea para la tabla (superior, intermedia o inferior)
  const generateTableLine = (columnSizes, position) => {
    const line = Object.keys(columnSizes)
      .map((columnIndex) => '═'.repeat(columnSizes[columnIndex]))
      .join(position === 'top' ? '╦' : position === 'middle' ? '╬' : '╩');

    return position === 'top' ? `╔${line}╗` : position === 'middle' ? `╠${line}╣` : `╚${line}╝`;
  };

  // Generar una fila de la tabla
  const generateTableRow = (rowData, columnSizes) => {
    return `║ ${Object.keys(columnSizes)
      .map(
        (columnIndex) =>
          `${`${rowData[columnIndex]}`.trim().padEnd(columnSizes[columnIndex] - 2, ' ').padStart(1, ' ')}`
      )
      .join(' ║ ')} ║`;
  };

  return (
    <div className='container-fluid'>
      <div className='row '>
        <div className='col-6 py-1'>
          <h5>Editor</h5>
          <Editor
            width='100%'
            height='500px'
            language='sql'
            theme='vs-dark'
            onChange={(value) => setSqlQuery(value)}
          />
        </div>
        <div className='col-6 py-1'>
          <h5>Salida</h5>
          <Editor
            width='100%'
            height='500px'
            language='plaintext'
            theme='vs-dark'
            options={{
              readOnly: true,
              wordWrap: 'on',
            }}
            value={queryResult}
          />
        </div>
        <div className='col-12 '>
          <h5>Consola</h5>
          <Editor
            width='100%'
            height='200px'
            language='plaintext'
            theme='vs-dark'
            options={{
              readOnly: true,
              wordWrap: 'on',
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default ConsoleIn;