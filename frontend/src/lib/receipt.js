import jsPDF from 'jspdf';

export function downloadReceiptPdf(order) {
  const doc = new jsPDF();

  doc.setFontSize(18);
  doc.text('Stock Smart — Order Receipt', 14, 20);

  doc.setFontSize(11);
  doc.text(`Order #${order.id}`, 14, 32);
  doc.text(`Date: ${order.timestamp}`, 14, 39);

  let y = 52;
  doc.setFont(undefined, 'bold');
  doc.text('Item', 14, y);
  doc.text('Qty', 120, y);
  doc.text('Price', 160, y);
  doc.setFont(undefined, 'normal');
  y += 8;

  order.items.forEach(({ item, qty, price }) => {
    doc.text(String(item), 14, y);
    doc.text(String(qty), 120, y);
    doc.text(`$${(price ?? 0).toFixed(2)}`, 160, y);
    y += 7;
  });

  y += 6;
  doc.setFont(undefined, 'bold');
  doc.text(`Total: $${order.total.toFixed(2)}`, 14, y);

  doc.save(`receipt-order-${order.id}.pdf`);
}
