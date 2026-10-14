const T = "#05010f";
const trazo = { stroke: T, strokeWidth: 4, strokeLinejoin: "round", strokeLinecap: "round" };
const fino = { stroke: T, strokeWidth: 3, strokeLinejoin: "round", strokeLinecap: "round" };
const METAL = "#8f9bc4";
const OSCURO = "#5d6894";
const OXIDO = "#ff9a1f";

export default function Mascota({ estado = "listo" }) {
  // El color de los ojos y del medidor cambia según el estado del chat
  const luz = estado === "error" ? "#ff4fa8" : estado === "rechazo" ? "#ffd93b" : "#9dff3c";

  return (
    <svg
      className={`mascota ${estado}`}
      viewBox="0 0 270 230"
      role="img"
      aria-label="Un robot de chatarra con mala cara"
    >
      <ellipse cx="135" cy="217" rx="84" ry="9" fill="rgba(0,0,0,0.4)" />

      {/* planeta y estrellas de fondo */}
      <circle cx="38" cy="40" r="15" fill="#ff4fa8" {...fino} />
      <ellipse cx="38" cy="40" rx="27" ry="7" fill="none" stroke="#2ee6f2" strokeWidth="4" transform="rotate(-20 38 40)" />
      <circle cx="248" cy="60" r="3" fill="#ffd93b" />
      <circle cx="250" cy="150" r="2.5" fill="#fff" />
      <circle cx="22" cy="130" r="2.5" fill="#9dff3c" />

      <g className="conjunto">
        {/* tubos de escape con humo */}
        <rect x="84" y="80" width="11" height="28" rx="4" fill={OSCURO} {...fino} />
        <rect x="175" y="80" width="11" height="28" rx="4" fill={OSCURO} {...fino} />
        <circle cx="89" cy="72" r="6" fill="rgba(255,255,255,0.35)" />
        <circle cx="95" cy="62" r="4" fill="rgba(255,255,255,0.22)" />
        <circle cx="181" cy="72" r="6" fill="rgba(255,255,255,0.35)" />
        <circle cx="175" cy="62" r="4" fill="rgba(255,255,255,0.22)" />

        {/* brazo izquierdo con pinza */}
        <rect x="62" y="106" width="22" height="50" rx="8" fill={METAL} {...trazo} />
        <path d="M64 154 L58 178 L70 168 L73 182 L80 166 L90 176 L84 154 Z" fill={OSCURO} {...trazo} />

        {/* brazo derecho (el que saluda) */}
        <g className="saludo">
          <rect x="184" y="66" width="22" height="50" rx="8" fill={METAL} {...trazo} />
          <path d="M184 68 L178 48 L190 58 L195 42 L200 58 L212 48 L206 68 Z" fill={OSCURO} {...trazo} />
        </g>

        {/* piernas y botas */}
        <rect x="100" y="168" width="26" height="34" rx="5" fill={OSCURO} {...trazo} />
        <rect x="144" y="168" width="26" height="34" rx="5" fill={OSCURO} {...trazo} />
        <rect x="90" y="198" width="42" height="14" rx="6" fill={METAL} {...trazo} />
        <rect x="138" y="198" width="42" height="14" rx="6" fill={METAL} {...trazo} />

        {/* torso */}
        <path d="M86 100 L184 100 L174 174 L96 174 Z" fill={METAL} {...trazo} />
        <path d="M97 158 Q108 150 114 160 Q106 170 99 167 Z" fill={OXIDO} stroke={T} strokeWidth="2.5" strokeLinejoin="round" />
        <rect x="108" y="116" width="54" height="40" rx="5" fill="#241a4d" {...fino} />
        <circle cx="126" cy="136" r="10" fill={luz} {...fino} />
        <line x1="126" y1="136" x2="131" y2="130" stroke={T} strokeWidth="2.5" strokeLinecap="round" />
        <line x1="144" y1="124" x2="156" y2="124" stroke="#cfd8ff" strokeWidth="3" strokeLinecap="round" />
        <line x1="144" y1="132" x2="156" y2="132" stroke="#cfd8ff" strokeWidth="3" strokeLinecap="round" />
        <line x1="144" y1="140" x2="156" y2="140" stroke="#cfd8ff" strokeWidth="3" strokeLinecap="round" />
        <circle cx="94" cy="108" r="3" fill="#cfd8ff" stroke={T} strokeWidth="2" />
        <circle cx="176" cy="108" r="3" fill="#cfd8ff" stroke={T} strokeWidth="2" />
        <circle cx="101" cy="166" r="3" fill="#cfd8ff" stroke={T} strokeWidth="2" />
        <circle cx="169" cy="166" r="3" fill="#cfd8ff" stroke={T} strokeWidth="2" />

        {/* cuello de resorte */}
        <rect x="118" y="84" width="34" height="18" rx="4" fill={OSCURO} {...fino} />
        <path d="M120 90 H150 M120 96 H150" fill="none" stroke={T} strokeWidth="2.5" />

        {/* cabeza ladeada */}
        <g transform="rotate(-3 135 62)">
          {/* antena torcida y antena rota */}
          <path d="M152 40 L156 26 L148 18" fill="none" {...trazo} />
          <circle className="luz" cx="147" cy="14" r="5" fill="#ff4fa8" {...fino} />
          <path d="M112 40 L108 31" fill="none" {...trazo} />
          <path d="M103 25 L108 31 L101 33 M113 26 L108 31" fill="none" stroke="#ffd93b" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />

          <path d="M96 40 L174 40 L168 86 L102 86 Z" fill={METAL} {...trazo} />

          {/* ojo grande con ceja de enojo */}
          <circle cx="118" cy="60" r="15" fill="#1a1030" {...fino} />
          <circle cx="118" cy="61" r="10" fill={luz} stroke={T} strokeWidth="2" />
          <circle cx="121" cy="63" r="4" fill={T} />
          <path d="M101 42 L101 46 L136 60 L136 42 Z" fill={METAL} />
          <line x1="101" y1="46" x2="136" y2="60" stroke={T} strokeWidth="4" strokeLinecap="round" />

          {/* ojo pequeño, desparejo */}
          <circle cx="153" cy="65" r="8" fill="#1a1030" {...fino} />
          <circle cx="153" cy="66" r="5" fill={luz} />
          <path d="M143 62 L170 52 L170 42 L143 42 Z" fill={METAL} />
          <line x1="143" y1="62" x2="170" y2="52" stroke={T} strokeWidth="4" strokeLinecap="round" />

          {/* grieta */}
          <path d="M139 46 L143 53 L138 59 L142 66" fill="none" stroke={T} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />

          {/* boca de dientes de sierra */}
          <rect x="110" y="72" width="54" height="11" rx="3" fill="#0a0520" {...fino} />
          <path d="M113 74 L119 82 L125 74 L131 82 L137 74 L143 82 L149 74 L155 82 L161 74" fill="none" stroke="#cfd8ff" strokeWidth="2.5" strokeLinejoin="round" />
        </g>
      </g>
    </svg>
  );
}