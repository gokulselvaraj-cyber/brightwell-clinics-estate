export default function QueuePosition({ position }: { position?: number | null }) {
  if (!position) return null;
  return <p className="queue">You are number {position} in the queue. Please take a seat.</p>;
}
