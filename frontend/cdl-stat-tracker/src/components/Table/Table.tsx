import * as React from 'react';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

interface RowData {
  player: string;
  kill: number;
  death: number;
  kd: number;
}

interface TableProps {
  rows: RowData[];
}

export default function CustomizedTables({ rows }: TableProps) {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 700 }} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Player</StyledTableCell>
            <StyledTableCell align="right">Kill</StyledTableCell>
            <StyledTableCell align="right">Death</StyledTableCell>
            <StyledTableCell align="right">KD</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row: RowData) => (
            <StyledTableRow key={row.player}>
              <StyledTableCell component="th" scope="row">
                {row.player}
              </StyledTableCell>
              <StyledTableCell align="right">{row.kill}</StyledTableCell>
              <StyledTableCell align="right">{row.death}</StyledTableCell>
              <StyledTableCell align="right">{row.kd}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}