import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Trophy, Code2, Loader2, PlayCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

interface Challenge {
  id: number;
  title: string;
  difficulty: string;
  is_recommended: boolean;
  is_solved: boolean;
}

export default function Challenges() {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/challenges`, { withCredentials: true });
      setChallenges(response.data.challenges);
    } catch (err) {
      setError('Failed to load challenges.');
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyColor = (diff: string) => {
    switch(diff.toLowerCase()) {
      case 'easy': return 'text-green-500 bg-green-500/10 border-green-500/20';
      case 'medium': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
      case 'hard': return 'text-red-500 bg-red-500/10 border-red-500/20';
      default: return 'text-primary bg-primary/10 border-primary/20';
    }
  };

  if (loading) return <div className="flex h-[calc(100vh-4rem)] items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>;
  if (error) return <div className="text-center mt-20 text-destructive">{error}</div>;

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-primary/20 rounded-xl">
          <Code2 className="w-8 h-8 text-primary" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-foreground">Coding Challenges</h1>
          <p className="text-muted-foreground">Test your skills and level up your programming logic.</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {challenges.map((challenge) => (
          <Link 
            key={challenge.id} 
            to={`/challenge/${challenge.id}`}
            className="group block"
          >
            <div className={`glass p-6 rounded-2xl h-full transition-all duration-300 hover:-translate-y-1 hover:shadow-xl relative overflow-hidden border ${challenge.is_solved ? 'border-green-500/30' : 'border-border'}`}>
              
              {challenge.is_solved && (
                <div className="absolute top-0 right-0 p-4">
                  <div className="bg-green-500/20 text-green-500 p-2 rounded-full">
                    <Trophy className="w-4 h-4" />
                  </div>
                </div>
              )}
              
              {challenge.is_recommended && !challenge.is_solved && (
                <div className="absolute top-0 right-0 p-4">
                  <div className="bg-yellow-500/20 text-yellow-500 p-2 rounded-full" title="Recommended to retry">
                    <AlertCircle className="w-4 h-4" />
                  </div>
                </div>
              )}

              <div className="mb-4">
                <span className={`px-3 py-1 text-xs font-semibold rounded-full border uppercase tracking-wider ${getDifficultyColor(challenge.difficulty)}`}>
                  {challenge.difficulty}
                </span>
              </div>
              
              <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors pr-8">
                {challenge.title}
              </h3>
              
              <div className="mt-6 flex items-center text-sm font-medium text-primary group-hover:text-primary/80">
                {challenge.is_solved ? 'Solve again' : 'Start challenge'}
                <PlayCircle className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
