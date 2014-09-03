module ApplicationHelper

  # Retorna data no formato dd/mm/yyyy
  def formatarData data
    data[8..9]+'/'+data[5..6]+'/'+data[0..3]
  end

  # Substitui ((NG))texto((CL)) por <b>texto</b>
  def tagNegrito s
    s.gsub(/(\(\(NG\)\)((?!\(\(NG\)\)).)*\(\(CL\)\))/i){|m|m.gsub(/\(\(NG\)\)/i,'<b>').gsub(/\(\(CL\)\)/i,'</b>')}
  end

  # Substitui ((TITULO))titulo((TEXTO)) por <h4><b>titulo</b></h4>
  def tagTitulo s
    s.gsub(/(\(\(TITULO\)\)((?!\(\(TITULO\)\)).)*\(\(TEXTO\)\))/i){|m|m.gsub(/\(\(TITULO\)\)/i,'<h4><b>').gsub(/\(\(TEXTO\)\)/i,'</b></h4>')}
  end

  # Substitui ((tag)) por ''
  def retirarTags s
    s.gsub(/\(\(NG\)\)/i,'').gsub(/\(\(CL\)\)/i,'').gsub(/\(\(TITULO\)\)/i,'').gsub(/\(\(TEXTO\)\)/i,'')
  end

  # Retorna texto com formatacao HTML
  def textoFormatado s
    retirarTags(tagTitulo(tagNegrito(s.gsub(/\n/, '<br />')))).html_safe
  end

  # Retorna texto sem formatacao HTML
  def textoNaoFormatado(s, tags=nil)
    # Primeiro coloca as tags HTML depois as tira.
    # Tira todas tags exceto as contidas em 'tags' - Por exemplo <em> para o Highlight das palavras buscadas.
    ActionController::Base.helpers.sanitize(textoFormatado(s).gsub(/(\<br \/\>)/,'<br /> '), :tags=>tags)
  end

def reject_param(url, param_to_reject, val=nil)
	require 'cgi'
	uri = URI(url) #=> #<URI::HTTP:0x007fbe25141a78 URL:http://example.com/path?param1=one&param2=2&param3=something3>
	params = CGI.parse(uri.query) #=> {"param1"=>["one"], "param2"=>["2"], "param3"=>["something3"]}
	if !val.nil?
	  params[param_to_reject].delete(val) if params[param_to_reject]
	else
	  params.delete(param_to_reject)
	end
	uri.query = URI.encode_www_form(params) #=> "param2=2&param3=something3"
	uri.to_s #=> "http://example.com/path?param2=2&param3=something3"
end


end
