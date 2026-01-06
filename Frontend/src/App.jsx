import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Volume2, Send, Eye, RefreshCw } from 'lucide-react';
import OracleEye from './components/OracleEye';
import { API_URL } from './config';

function App() {
  const [status, setStatus] = useState('idle'); // idle, loading, active, success, failure
  const [data, setData] = useState(null); // { image_url, audio_url, labels }
  const [guess, setGuess] = useState('');
  const [feedback, setFeedback] = useState('');
  const [attempts, setAttempts] = useState(3);
  const [imageRevealed, setImageRevealed] = useState(false);
  const audioRef = useRef(null);

  const summonOracle = async () => {
    setStatus('loading');
    setFeedback('');
    setGuess('');
    setAttempts(3);
    setImageRevealed(false);
    try {
      const res = await fetch(`${API_URL}/init`, { method: 'POST' });
      if (!res.ok) throw new Error('Error al invocar al Oráculo');
      const result = await res.json();

      // URLs ahora vienen directamente de S3 como absolutas
      setData(result);
      setStatus('active');
    } catch (err) {
      console.error(err);
      setFeedback("El Oráculo guarda silencio... (Error al conectar con el servidor)");
      setStatus('idle');
    }
  };

  const submitGuess = async (e) => {
    e.preventDefault();
    if (!guess.trim()) return;

    try {
      const res = await fetch(`${API_URL}/guess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ guess, labels: data.labels })
      });
      const result = await res.json();

      setFeedback(result.mensaje_esfinge);
      if (result.resultado === 'correcto' || result.resultado === 'sinonimo') {
        setStatus('success');
        setImageRevealed(true);
      } else {
        const newAttempts = attempts - 1;
        setAttempts(newAttempts);
        if (newAttempts <= 0) {
          setStatus('failure');
          setImageRevealed(true);
        } else {
          // Keep active to allow retries
          setStatus('active');
        }
      }
    } catch (err) {
      console.error(err);
      setFeedback("Los vientos se llevan tus palabras... (Error al enviar respuesta)");
    }
  };

  useEffect(() => {
    if (status === 'active' && data?.audio_url && audioRef.current) {
      audioRef.current.play().catch(e => console.log("Audio autoplay blocked", e));
    }
  }, [status, data]);

  return (
    <div className="app-container">
      <header className="flex-center" style={{ padding: '2rem', flexDirection: 'column' }}>
        <h1 style={{ fontSize: '3rem', textShadow: 'var(--glow-gold)' }}>El Oráculo Secreto</h1>
        <p style={{ color: 'var(--color-gold-dim)', marginTop: '0.5rem' }}>La Esfinge Griega</p>
      </header>

      <main className="container flex-center" style={{ flexDirection: 'column', gap: '2rem' }}>

        <OracleEye state={status} />

        <AnimatePresence mode="wait">
          {status === 'idle' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <button
                onClick={summonOracle}
                className="mystical-border"
                style={{
                  padding: '1rem 3rem',
                  fontSize: '1.5rem',
                  background: 'transparent',
                  color: 'var(--color-gold)',
                  borderRadius: '50px',
                  transition: 'all 0.3s'
                }}
                onMouseOver={(e) => e.currentTarget.style.background = 'rgba(212, 175, 55, 0.1)'}
                onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
              >
                Invocar al Oráculo <Sparkles style={{ display: 'inline', marginLeft: '10px' }} />
              </button>
            </motion.div>
          )}

          {(status === 'loading') && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              style={{ fontSize: '1.2rem', fontStyle: 'italic' }}
            >
              Consultando las estrellas...
            </motion.p>
          )}

          {(status === 'active' || status === 'success' || status === 'failure') && data && (
            <motion.div
              className="oracle-interface"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              style={{ width: '100%', maxWidth: '600px', textAlign: 'center' }}
            >
              <div className="image-container mystical-border" style={{ padding: '10px', background: 'rgba(0,0,0,0.3)', marginBottom: '2rem', position: 'relative', minHeight: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {imageRevealed ? (
                  <img src={data.image_url} alt="Visión del Oráculo" style={{ width: '100%', display: 'block' }} />
                ) : (
                  <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--color-mystic)' }}>
                    <p>La visión está nublada...</p>
                    <button
                      type="button"
                      onClick={() => setImageRevealed(true)}
                      style={{
                        marginTop: '1rem',
                        padding: '0.5rem 1rem',
                        background: 'transparent',
                        border: '1px solid var(--color-gold)',
                        color: 'var(--color-gold)',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px',
                        margin: '1rem auto'
                      }}
                    >
                      <Eye size={16} /> Mostrar Imagen
                    </button>
                  </div>
                )}
              </div>

              <audio ref={audioRef} src={data.audio_url} controls style={{ width: '100%', marginBottom: '2rem' }} />

              <form onSubmit={submitGuess} style={{ display: 'flex', gap: '10px' }}>
                <input
                  type="text"
                  value={guess}
                  onChange={(e) => setGuess(e.target.value)}
                  placeholder="¿Cuál es el secreto?"
                  style={{
                    flex: 1,
                    padding: '1rem',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid var(--color-mystic)',
                    color: 'var(--color-ethereal)',
                    fontSize: '1.2rem',
                    fontFamily: 'var(--font-heading)'
                  }}
                  disabled={status === 'failure' || status === 'success'}
                />
                <button
                  type="submit"
                  disabled={status === 'failure' || status === 'success'}
                  style={{
                    padding: '0 2rem',
                    background: status === 'failure' || status === 'success' ? 'grey' : 'var(--color-gold)',
                    cursor: status === 'failure' || status === 'success' ? 'not-allowed' : 'pointer',
                    color: 'var(--color-void)',
                    fontWeight: 'bold',
                    fontSize: '1.2rem'
                  }}
                >
                  <Send />
                </button>
              </form>

              <div style={{ marginTop: '1rem', color: 'var(--color-gold-dim)' }}>
                Intentos restantes: {attempts}
              </div>

              {feedback && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  key={feedback} // Re-animate on feedback change
                  style={{
                    marginTop: '2rem',
                    padding: '1rem',
                    border: `1px solid ${status === 'success' ? 'var(--color-oracle)' : 'var(--color-error)'}`,
                    background: 'rgba(0,0,0,0.5)',
                    color: status === 'success' ? 'var(--color-oracle)' : 'var(--color-error)',
                    fontFamily: 'var(--font-heading)',
                    fontSize: '1.2rem'
                  }}
                >
                  {feedback}
                </motion.div>
              )}

              {(status === 'success' || status === 'failure') && (
                <button
                  onClick={summonOracle}
                  style={{
                    marginTop: '2rem',
                    padding: '1rem 2rem',
                    background: 'transparent',
                    border: '1px solid var(--color-gold)',
                    color: 'var(--color-gold)',
                    cursor: 'pointer',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '10px'
                  }}
                >
                  <RefreshCw /> {status === 'success' ? 'Consultar de nuevo' : 'Volver a jugar'}
                </button>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
