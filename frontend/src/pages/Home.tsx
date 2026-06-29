import { Link } from 'react-router-dom';
import { ArrowRight, Code2, Sparkles, Terminal } from 'lucide-react';

export default function Home() {
  return (
    <div className="relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/50 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/50 blur-[120px] pointer-events-none" />
      
      <div className="container mx-auto px-4 pt-32 pb-24 relative z-10">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="inline-flex items-center space-x-2 bg-primary/10 text-primary border border-primary/20 px-4 py-1.5 rounded-full text-sm font-medium mb-4 animate-in fade-in slide-in-from-bottom-4 duration-1000">
            <Sparkles className="w-4 h-4" />
            <span>Next-Generation AI Coding Assistant</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-foreground animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-150">
            Master Code Faster with
            <br />
            <span className="text-muted-foreground">CodeMentor AI</span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-300">
            Elevate your programming skills with real-time AI feedback, smart code analysis, and interactive challenges tailored to your learning pace.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-500">
            <Link to="/register" className="group flex items-center gap-2 px-8 py-4 bg-primary text-primary-foreground rounded-xl font-semibold text-lg hover:bg-primary/90 transition-all hover:scale-105 active:scale-95 shadow-lg border border-border">
              Start Coding Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link to="/login" className="px-8 py-4 bg-secondary text-secondary-foreground rounded-xl font-semibold text-lg hover:bg-secondary/80 transition-all">
              Sign In
            </Link>
          </div>
        </div>

        <div className="mt-24 grid md:grid-cols-3 gap-8">
          <FeatureCard 
            icon={<Code2 className="w-8 h-8 text-foreground" />}
            title="Smart Analysis"
            description="Get instant feedback on your code syntax, structure, and potential bugs using advanced AI models."
          />
          <FeatureCard 
            icon={<Terminal className="w-8 h-8 text-foreground" />}
            title="Interactive Challenges"
            description="Practice with hands-on coding challenges designed to test your knowledge and improve your skills."
          />
          <FeatureCard 
            icon={<Sparkles className="w-8 h-8 text-foreground" />}
            title="Voice Commands"
            description="Use your voice to dictate code and commands with our cutting-edge Whisper AI integration."
          />
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="glass p-8 rounded-2xl flex flex-col space-y-4 hover:-translate-y-2 transition-transform duration-300">
      <div className="w-16 h-16 rounded-xl bg-secondary flex items-center justify-center border border-border">
        {icon}
      </div>
      <h3 className="text-xl font-bold">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">
        {description}
      </p>
    </div>
  );
}
