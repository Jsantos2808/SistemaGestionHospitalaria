export interface LoginResponse {
  access_token: string;
  token_type: string;
  username: string;
  rol: string;
  nombre: string;
}

export interface Paciente {
  id_paciente: number;
  nombre: string;
  apellido: string;
  fecha_nacimiento: string;
  telefono: string;
  email: string;
  direccion: string;
  tipo_sangre: string;
}

export type PacientePayload = Omit<Paciente, 'id_paciente'>;

export interface Medico {
  id_medico: number;
  especialidad: string;
  numero_licencia: string;
  nombre: string;
}

export interface Cita {
  id_cita: number;
  id_paciente: number;
  id_medico: number;
  fecha_hora: string;
  estado: string;
  motivo: string;
  paciente_nombre?: string;
  medico_nombre?: string;
  especialidad?: string;
}

export interface CitaPayload {
  id_paciente: number;
  id_medico: number;
  fecha_hora: string;
  motivo: string;
  estado: string;
}

export interface Historial {
  id_historial: number;
  id_paciente: number;
  id_medico: number;
  fecha_visita: string;
  diagnostico: string;
  tratamiento: string;
  notas_adicionales?: string;
  paciente_nombre?: string;
  medico_nombre?: string;
}

export interface HistorialPayload {
  id_paciente: number;
  id_medico: number;
  fecha_visita: string;
  diagnostico: string;
  tratamiento: string;
  notas_adicionales: string;
}

export interface DashboardStats {
  total_pacientes: number;
  citas_hoy: number;
  citas_programadas: number;
  total_historiales: number;
}
